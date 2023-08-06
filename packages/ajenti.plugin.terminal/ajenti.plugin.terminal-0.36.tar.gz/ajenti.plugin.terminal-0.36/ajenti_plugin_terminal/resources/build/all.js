'use strict';

angular.module('ajenti.terminal', ['core', 'ajenti.ace']);


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/terminal', {
        templateUrl: '/terminal:resources/partial/index.html',
        controller: 'TerminalIndexController'
    });

    return $routeProvider.when('/view/terminal/:id', {
        templateUrl: '/terminal:resources/partial/view.html',
        controller: 'TerminalViewController'
    });
});


'use strict';

var colors = {
    normal: {
        black: '#073642',
        white: '#eee8d5',
        green: '#859900',
        brown: '#af8700',
        red: '#dc322f',
        magenta: '#d33682',
        violet: '#6c71c4',
        blue: '#268bd2',
        cyan: '#2aa198'
    },
    bright: {
        black: '#074a5c',
        white: '#f6f2e6',
        green: '#bbd320',
        brown: '#efbc10',
        red: '#e5423f',
        magenta: '#dd458f',
        violet: '#7a7fd0',
        blue: '#3198e1',
        cyan: '#2abbb0'
    }
};

angular.module('ajenti.terminal').directive('terminal', function ($timeout, $log, $q, socket, notify, terminals, hotkeys, gettext) {
    return {
        scope: {
            id: '=?',
            onReady: '&?',
            textData: '=?'
        },
        template: '<div>\n<canvas></canvas>\n<div class="paste-area" ng:class="{focus: pasteAreaFocused}">\n    <i class="fa fa-paste"></i>\n    <span ng:show="pasteAreaFocused">\n        Paste now\n    </span>\n\n    <textarea\n        ng:model="pasteData"\n        ng:focus="pasteAreaFocused = true"\n        ng:blur="pasteAreaFocused = false"\n    ></textarea>\n</div>\n\n<textarea\n    class="mobile-input-area"\n    ng:if="isMobile"\n    autocomplete="off"\n    autocorrect="off"\n    autocapitalize="off"\n    spellcheck="false"\n></textarea>\n\n<a class="extra-keyboard-toggle btn btn-default" ng:click="extraKeyboardVisible=!extraKeyboardVisible" ng:show="isMobile">\n    <i class="fa fa-keyboard-o"></i>\n</a>\n\n<div class="extra-keyboard" ng:show="extraKeyboardVisible">\n    <a class="btn btn-default" ng:click="extraKeyboardCtrl = true" ng:class="{active: extraKeyboardCtrl}">\n        Ctrl\n    </a>\n    <a class="btn btn-default" ng:click="fakeKeyEvent(38)">\n        <i class="fa fa-arrow-up"></i>\n    </a>\n    <a class="btn btn-default" ng:click="fakeKeyEvent(40)">\n        <i class="fa fa-arrow-down"></i>\n    </a>\n    <a class="btn btn-default" ng:click="fakeKeyEvent(37)">\n        <i class="fa fa-arrow-left"></i>\n    </a>\n    <a class="btn btn-default" ng:click="fakeKeyEvent(39)">\n        <i class="fa fa-arrow-right"></i>\n    </a>\n</div>\n</div>',
        link: function link($scope, element, attrs) {
            element.addClass('block-element');

            $scope.isMobile = new MobileDetect(window.navigator.userAgent).mobile();
            $scope.extraKeyboardVisible = false;

            $scope.charWidth = 7;
            $scope.charHeight = 14;
            $scope.canvas = element.find('canvas')[0];
            $scope.context = $scope.canvas.getContext('2d');
            $scope.font = '12px monospace';
            $scope.ready = false;
            $scope.textLines = [];
            $scope.pasteData = null;

            $scope.clear = function () {
                $scope.dataWidth = 0;
                $scope.dataHeight = 0;
            };

            $scope.fullReload = function () {
                return terminals.full($scope.id).then(function (data) {
                    if (!data) {
                        return $q.reject();
                    }

                    socket.send('terminal', {
                        action: 'subscribe',
                        id: $scope.id
                    });

                    $scope.clear();
                    $scope.draw(data);

                    if (!$scope.ready) {
                        $scope.ready = true;
                        $scope.onReady();
                        $timeout(function () {
                            return (// reflow
                                $scope.autoResize()
                            );
                        });
                    }
                });
            };

            $scope.clear();
            $scope.fullReload().catch(function () {
                $scope.disabled = true;
                $scope.onReady();
                notify.info(gettext('Terminal was closed'));
            });

            $scope.scheduleResize = function (w, h) {
                $timeout.cancel($scope.resizeTimeout);
                $scope.resizeTimeout = $timeout(function () {
                    return $scope.resize(w, h);
                }, 1000);
            };

            $scope.resize = function (w, h) {
                socket.send('terminal', {
                    action: 'resize',
                    id: $scope.id,
                    width: w,
                    height: h
                });
                $scope.canvas.width = $scope.charWidth * w;
                $scope.canvas.height = $scope.charHeight * h;
                $scope.fullReload();
            };

            $scope.autoResize = function () {
                var availableWidth = element.parent().width() - 40;
                var availableHeight = $(window).height() - 60 - 40;
                var cols = Math.floor(availableWidth / $scope.charWidth);
                var rows = Math.floor(availableHeight / $scope.charHeight);
                $scope.scheduleResize(cols, rows);
            };

            $scope.$on('window:resize', $scope.autoResize);

            $scope.$on('navigation:toggle', function () {
                return $timeout(function () {
                    return (// reflow
                        $scope.autoResize()
                    );
                });
            });

            $scope.$on('widescreen:toggle', function () {
                return $timeout(function () {
                    return (// reflow
                        $scope.autoResize()
                    );
                });
            });

            $scope.$on('terminal:paste', function () {
                return element.find('textarea').focus();
            });

            $scope.$on('socket:terminal', function ($event, data) {
                if (data.id !== $scope.id || $scope.disabled) {
                    return;
                }
                if (data.type === 'closed') {
                    $scope.disabled = true;
                    notify.info(gettext('Terminal was closed'));
                }
                if (data.type === 'data') {
                    $scope.draw(data.data);
                }
            });

            $scope.draw = function (data) {
                //console.log 'Payload', data

                if ($scope.dataWidth !== data.w || $scope.dataHeight !== data.h) {
                    $scope.dataWidth = data.w;
                    $scope.dataHeight = data.h;
                }

                $scope.cursor = data.cursor;
                if (data.cursor) {
                    $scope.cursx = data.cx;
                    $scope.cursy = data.cy;
                } else {
                    $scope.cursx = -1;
                }

                $scope.context.font = $scope.font;
                $scope.context.textBaseline = 'top';

                for (var y in data.lines) {
                    var row = data.lines[y];
                    var line = '';

                    for (var x in row) {
                        var cell = row[x];
                        if (cell) {
                            line += cell[0];
                        }
                    }
                    $scope.textLines[parseInt(y)] = line;
                }

                $scope.textData = $scope.textLines.join('\n');

                var lns = element.find('div');
                for (y in data.lines) {
                    var _row = data.lines[y];
                    y = parseInt(y);

                    $scope.context.fillStyle = colors.normal.black;
                    $scope.context.fillRect(0, $scope.charHeight * y, $scope.charWidth * $scope.dataWidth, $scope.charHeight);

                    for (var _x = 0; _x < _row.length; _x++) {
                        var _cell = _row[_x];

                        if (!_cell) {
                            continue;
                        }

                        var defaultFG = 'white';
                        var defaultBG = 'black';

                        if (_cell[7]) {
                            // reverse
                            var t = _cell[1];
                            _cell[1] = _cell[2];
                            _cell[2] = t;
                            defaultFG = 'black';
                            defaultBG = 'white';
                        }

                        if (_cell[3]) {
                            $scope.context.font = 'bold ' + $scope.context.font;
                        }
                        if (_cell[4]) {
                            $scope.context.font = 'italic ' + $scope.context.font;
                        }

                        if (_cell[2]) {
                            if (_cell[2] !== 'default' || _cell[7]) {
                                $scope.context.fillStyle = colors.normal[_cell[2]] || colors.normal[defaultBG];
                                $scope.context.fillRect($scope.charWidth * _x, $scope.charHeight * y, $scope.charWidth, $scope.charHeight);
                            }
                        }

                        if (y === $scope.cursy && _x === $scope.cursx) {
                            $scope.context.fillStyle = colors.normal['white'];
                            $scope.context.fillRect($scope.charWidth * _x, $scope.charHeight * y, $scope.charWidth, $scope.charHeight);
                        }

                        if (_cell[1]) {
                            var colorMap = _cell[3] ? colors.bright : colors.normal;
                            $scope.context.fillStyle = colorMap[_cell[1]] || colorMap[defaultFG];
                            $scope.context.fillText(_cell[0], $scope.charWidth * _x, $scope.charHeight * y);
                            if (_cell[5]) {
                                $scope.context.fillRect($scope.charWidth * _x, $scope.charHeight * (y + 1) - 1, $scope.charWidth, 1);
                            }
                        }

                        if (_cell[3] || _cell[4]) {
                            $scope.context.font = $scope.font;
                        }
                    }
                }
            };

            $scope.parseKey = function (event, event_name, ign_arrows) {
                var ch = null;

                if (event.ctrlKey && event.keyCode === 17) {
                    // ctrl-V
                    return;
                }

                if (event.ctrlKey && event.keyCode > 64) {
                    return String.fromCharCode(event.keyCode - 64);
                }

                //$log.log event

                if (event_name === 'keypress' && (event.charCode || event.which)) {
                    ch = String.fromCharCode(event.which);
                    if (ch === '\r') {
                        ch = '\n';
                    }
                    return ch;
                }

                if (event_name === 'keydown' && event.keyCode >= 112 && event.keyCode <= 123) {
                    var fNumber = event.keyCode - 111;
                    switch (fNumber) {
                        case 1:
                            ch = '\x1bOP';
                            break;
                        case 2:
                            ch = '\x1bOQ';
                            break;
                        case 3:
                            ch = '\x1bOR';
                            break;
                        case 4:
                            ch = '\x1bOS';
                            break;
                        default:
                            ch = '\x1B[' + (fNumber + 10) + '~';
                    }
                    return ch;
                }

                switch (event.keyCode) {
                    case 8:
                        ch = '\b';
                        break;
                    case 9:
                        if (!ign_arrows) {
                            ch = '\t';
                        }
                        break;
                    case 13:case 10:
                        ch = '\r';
                        break;
                    case 38:
                        if (!ign_arrows) {
                            ch = '\x1b[A';
                        }
                        break;
                    case 40:
                        if (!ign_arrows) {
                            ch = '\x1b[B';
                        }
                        break;
                    case 39:
                        if (!ign_arrows) {
                            ch = '\x1b[C';
                        }
                        break;
                    case 37:
                        if (!ign_arrows) {
                            ch = '\x1b[D';
                        }
                        break;
                    case 35:
                        // END
                        ch = '\x1b[F';
                        break;
                    case 36:
                        // HOME
                        ch = '\x1b[H';
                        break;
                    case 34:
                        //PGUP
                        ch = '\x1b[6~';
                        break;
                    case 33:
                        //PGDN
                        ch = '\x1b[5~';
                        break;
                    case 27:
                        ch = '\x1b';
                        break;
                }

                return ch || null;
            };

            $scope.sendInput = function (data) {
                return socket.send('terminal', {
                    action: 'input',
                    id: $scope.id,
                    data: data
                });
            };

            var handler = function handler(key, event, mode) {
                if ($scope.pasteAreaFocused || $scope.disabled) {
                    return;
                }
                if ($scope.extraKeyboardCtrl) {
                    event.ctrlKey = true;
                    $scope.extraKeyboardCtrl = false;
                }
                var ch = $scope.parseKey(event, mode);
                if (!ch) {
                    return false;
                }
                $scope.sendInput(ch);
                return true;
            };

            hotkeys.on($scope, function (k, e) {
                return handler(k, e, 'keypress');
            }, 'keypress:global');

            hotkeys.on($scope, function (k, e) {
                return handler(k, e, 'keydown');
            }, 'keydown:global');

            $scope.fakeKeyEvent = function (code) {
                return handler(null, { keyCode: code }, 'keydown');
            };

            $scope.$watch('pasteData', function () {
                if ($scope.pasteData) {
                    $scope.sendInput($scope.pasteData);
                }
                $scope.pasteData = '';
                element.find('textarea').blur();
            });
        }
    };
});


'use strict';

angular.module('ajenti.terminal').controller('TerminalIndexController', function ($scope, $location, $q, pageTitle, terminals, gettext) {
    pageTitle.set(gettext('Terminals'));

    $scope.refresh = function () {
        return terminals.list().then(function (list) {
            $scope.terminals = list;
        });
    };

    $scope.create = function () {
        return terminals.create({ autoclose: true }).then(function (id) {
            return $location.path('/view/terminal/' + id);
        });
    };

    $scope.runCommand = function () {
        return terminals.create({ command: $scope.command, autoclose: true }).then(function (id) {
            return $location.path('/view/terminal/' + id);
        });
    };

    $scope.kill = function (terminal) {
        return terminals.kill(terminal.id).then(function () {
            return $scope.refresh();
        });
    };

    $scope.refresh();
});


'use strict';

angular.module('ajenti.terminal').controller('TerminalViewController', function ($scope, $routeParams, $interval, terminals, hotkeys, pageTitle) {
    pageTitle.set('Terminal');

    $scope.id = $routeParams.id;
    $scope.ready = false;
    $scope.copyData = '';
    $scope.copyDialogVisible = false;

    $scope.onReady = function () {
        return $scope.ready = true;
    };

    hotkeys.on($scope, function (k, e) {
        if (k === 'C' && e.ctrlKey && e.shiftKey) {
            $scope.copyDialogVisible = true;
            return true;
        }
        if (k === 'V' && e.ctrlKey && e.shiftKey) {
            $scope.$broadcast('terminal:paste');
            return true;
        }
        if (k === 'D' && e.ctrlKey) {
            terminals.kill($scope.id);
            return true;
        }
    });

    $scope.check = function () {
        terminals.is_dead($scope.id);
    };

    $scope.redirect_if_dead = $interval($scope.check, 4000, 0);

    $scope.$on('$destroy', function () {
        $interval.cancel($scope.redirect_if_dead);
    });

    $scope.hideCopyDialogVisible = function () {
        return $scope.copyDialogVisible = false;
    };
});


'use strict';

angular.module('ajenti.terminal').controller('ScriptWidgetController', function ($scope, $location, notify, terminals, gettext) {
    $scope.run = function () {
        var _$scope$widget$config = $scope.widget.config,
            script = _$scope$widget$config.script,
            input = _$scope$widget$config.input;

        if ($scope.widget.config.terminal) {
            terminals.create({ command: script, autoclose: true }).then(function (id) {
                return $location.path('/view/terminal/' + id);
            });
        } else {
            notify.info(gettext('Starting the script'), script.substring(0, 100) + '...');
            terminals.script({ script: script, input: input }).then(function (data) {
                if (data.code === 0) {
                    notify.success(gettext('Script has finished'), data.output + data.stderr);
                } else {
                    notify.warning(gettext('Script has failed'), data.stderr + data.output);
                }
            }).catch(function (err) {
                return notify.error(gettext('Could not launch the script'), err.message);
            });
        }
    };
});


'use strict';

angular.module('ajenti.terminal').service('terminals', function ($http, $q, $location, $timeout, notify, gettext) {
    this.script = function (options) {
        return $http.post('/api/terminal/script', options).then(function (response) {
            return response.data;
        });
    };

    this.list = function () {
        return $http.get("/api/terminal/list").then(function (response) {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = response.data[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var terminal = _step.value;

                    var cmd = terminal.command.split(' ')[0];
                    var tokens = cmd.split('/');
                    terminal.title = tokens[tokens.length - 1];
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }

            return response.data;
        });
    };

    this.kill = function (id) {
        return $http.get('/api/terminal/kill/' + id).then(function (response) {
            var redirect = response.data;
            notify.info(gettext('You will be redirect to the previous page.'));
            return $timeout(function () {
                return $location.path(redirect);
            }, 3000);
        });
    };

    this.is_dead = function (id) {
        var _this = this;

        return $http.get('/api/terminal/is_dead/' + id, { ignoreLoadingBar: true }).then(function (response) {
            if (response.data === true) {
                return _this.kill(id);
            };
        });
    };

    this.create = function (options) {
        if (typeof options === 'undefined' || options === null) {
            options = {};
        }
        return $http.post("/api/terminal/create", options).then(function (response) {
            return response.data;
        });
    };

    this.full = function (id) {
        return $http.get('/api/terminal/full/' + id).then(function (response) {
            return response.data;
        });
    };

    this.navigate = function (id) {
        return $location.path('/view/terminal/' + id);
    };

    return this;
});



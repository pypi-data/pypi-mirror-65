(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"), require("react-dom"));
	else if(typeof define === 'function' && define.amd)
		define(["react", "react-dom"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_renderer"] = factory(require("react"), require("react-dom"));
	else
		root["dazzler_renderer"] = factory(root["React"], root["ReactDOM"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"renderer": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonpdazzler_name_"] = window["webpackJsonpdazzler_name_"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([1,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/renderer/js/components/Renderer.jsx":
/*!*************************************************!*\
  !*** ./src/renderer/js/components/Renderer.jsx ***!
  \*************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _Updater__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Updater */ "./src/renderer/js/components/Updater.jsx");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_2__);
function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }





var Renderer = function Renderer(props) {
  var _useState = Object(react__WEBPACK_IMPORTED_MODULE_0__["useState"])(1),
      _useState2 = _slicedToArray(_useState, 2),
      reloadKey = _useState2[0],
      setReloadKey = _useState2[1]; // FIXME find where this is used and refactor/remove


  window.dazzler_base_url = props.baseUrl;
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
    className: "dazzler-renderer"
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_Updater__WEBPACK_IMPORTED_MODULE_1__["default"], _extends({}, props, {
    key: "upd-".concat(reloadKey),
    hotReload: function hotReload() {
      return setReloadKey(reloadKey + 1);
    }
  })));
};

Renderer.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_2___default.a.number
};
/* harmony default export */ __webpack_exports__["default"] = (Renderer);

/***/ }),

/***/ "./src/renderer/js/components/Updater.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Updater.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Updater; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _requests__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../requests */ "./src/renderer/js/requests.js");
/* harmony import */ var _hydrator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../hydrator */ "./src/renderer/js/hydrator.js");
/* harmony import */ var _requirements__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../requirements */ "./src/renderer/js/requirements.js");
/* harmony import */ var commons__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! commons */ "./src/commons/js/index.js");
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }









var Updater =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Updater, _React$Component);

  function Updater(props) {
    var _this;

    _classCallCheck(this, Updater);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Updater).call(this, props));
    _this.state = {
      layout: false,
      ready: false,
      page: null,
      bindings: {},
      packages: [],
      requirements: [],
      reloading: false,
      needRefresh: false
    }; // The api url for the page is the same but a post.
    // Fetch bindings, packages & requirements

    _this.pageApi = Object(_requests__WEBPACK_IMPORTED_MODULE_2__["apiRequest"])(window.location.href); // All components get connected.

    _this.boundComponents = {};
    _this.ws = null;
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    _this.connect = _this.connect.bind(_assertThisInitialized(_this));
    _this.disconnect = _this.disconnect.bind(_assertThisInitialized(_this));
    _this.onMessage = _this.onMessage.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Updater, [{
    key: "updateAspects",
    value: function updateAspects(identity, aspects) {
      var _this2 = this;

      return new Promise(function (resolve) {
        var aspectKeys = Object(ramda__WEBPACK_IMPORTED_MODULE_6__["keys"])(aspects);
        var bindings = aspectKeys.map(function (key) {
          return _objectSpread({}, _this2.state.bindings["".concat(key, "@").concat(identity)], {
            value: aspects[key]
          });
        }).filter(function (e) {
          return e.trigger;
        });

        _this2.state.rebindings.forEach(function (binding) {
          if (binding.trigger.identity.test(identity)) {
            bindings = Object(ramda__WEBPACK_IMPORTED_MODULE_6__["concat"])(bindings, aspectKeys.filter(function (k) {
              return binding.trigger.aspect.test(k);
            }).map(function (k) {
              return _objectSpread({}, binding, {
                value: aspects[k],
                trigger: _objectSpread({}, binding.trigger, {
                  identity: identity,
                  aspect: k
                })
              });
            }));
            bindings.push();
          }
        });

        if (!bindings) {
          console.log('binding');
          return resolve(0);
        }

        bindings.forEach(function (binding) {
          return _this2.sendBinding(binding, binding.value);
        });
        resolve(bindings.length);
      });
    }
  }, {
    key: "connect",
    value: function connect(identity, setAspects, getAspect, matchAspects) {
      this.boundComponents[identity] = {
        setAspects: setAspects,
        getAspect: getAspect,
        matchAspects: matchAspects
      };
    }
  }, {
    key: "disconnect",
    value: function disconnect(identity) {
      delete this.boundComponents[identity];
    }
  }, {
    key: "onMessage",
    value: function onMessage(response) {
      var _this3 = this;

      var data = JSON.parse(response.data);
      var identity = data.identity,
          kind = data.kind,
          payload = data.payload,
          storage = data.storage,
          request_id = data.request_id;
      var store;

      if (storage === 'session') {
        store = window.sessionStorage;
      } else {
        store = window.localStorage;
      }

      switch (kind) {
        case 'set-aspect':
          var setAspects = function setAspects(component) {
            return component.setAspects(Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["hydrateProps"])(payload, _this3.updateAspects, _this3.connect, _this3.disconnect)).then(function () {
              return _this3.updateAspects(identity, payload);
            });
          };

          if (data.regex) {
            var pattern = new RegExp(data.identity);
            Object(ramda__WEBPACK_IMPORTED_MODULE_6__["keys"])(this.boundComponents).filter(function (k) {
              return pattern.test(k);
            }).map(function (k) {
              return _this3.boundComponents[k];
            }).forEach(setAspects);
          } else {
            setAspects(this.boundComponents[identity]);
          }

          break;

        case 'get-aspect':
          var aspect = data.aspect;
          var wanted = this.boundComponents[identity];

          if (!wanted) {
            this.ws.send(JSON.stringify({
              kind: kind,
              identity: identity,
              aspect: aspect,
              request_id: request_id,
              error: "Aspect not found ".concat(identity, ".").concat(aspect)
            }));
            return;
          }

          var value = wanted.getAspect(aspect);
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            aspect: aspect,
            value: Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(value),
            request_id: request_id
          }));
          break;

        case 'set-storage':
          store.setItem(identity, JSON.stringify(payload));
          break;

        case 'get-storage':
          this.ws.send(JSON.stringify({
            kind: kind,
            identity: identity,
            request_id: request_id,
            value: JSON.parse(store.getItem(identity))
          }));
          break;

        case 'reload':
          var filenames = data.filenames,
              hot = data.hot,
              refresh = data.refresh,
              deleted = data.deleted;

          if (refresh) {
            this.ws.close();
            return this.setState({
              reloading: true,
              needRefresh: true
            });
          }

          if (hot) {
            // The ws connection will close, when it
            // reconnect it will do a hard reload of the page api.
            return this.setState({
              reloading: true
            });
          }

          filenames.forEach(_requirements__WEBPACK_IMPORTED_MODULE_4__["loadRequirement"]);
          deleted.forEach(function (r) {
            return Object(commons__WEBPACK_IMPORTED_MODULE_5__["disableCss"])(r.url);
          });
          break;

        case 'ping':
          // Just do nothing.
          break;
      }
    }
  }, {
    key: "sendBinding",
    value: function sendBinding(binding, value) {
      var _this4 = this;

      // Collect all values and send a binding payload
      var trigger = _objectSpread({}, binding.trigger, {
        value: Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(value)
      });

      var states = binding.states.reduce(function (acc, state) {
        if (state.regex) {
          var identityPattern = new RegExp(state.identity);
          var aspectPattern = new RegExp(state.aspect);
          return Object(ramda__WEBPACK_IMPORTED_MODULE_6__["concat"])(acc, Object(ramda__WEBPACK_IMPORTED_MODULE_6__["flatten"])(Object(ramda__WEBPACK_IMPORTED_MODULE_6__["keys"])(_this4.boundComponents).map(function (k) {
            var values = [];

            if (identityPattern.test(k)) {
              values = _this4.boundComponents[k].matchAspects(aspectPattern).map(function (_ref) {
                var _ref2 = _slicedToArray(_ref, 2),
                    name = _ref2[0],
                    val = _ref2[1];

                return _objectSpread({}, state, {
                  identity: k,
                  aspect: name,
                  value: Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(val)
                });
              });
            }

            return values;
          })));
        }

        acc.push(_objectSpread({}, state, {
          value: _this4.boundComponents[state.identity] && Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["prepareProp"])(_this4.boundComponents[state.identity].getAspect(state.aspect))
        }));
        return acc;
      }, []);
      var payload = {
        trigger: trigger,
        states: states,
        kind: 'binding',
        page: this.state.page,
        key: binding.key
      };
      this.ws.send(JSON.stringify(payload));
    }
  }, {
    key: "_connectWS",
    value: function _connectWS() {
      var _this5 = this;

      // Setup websocket for updates
      var tries = 0;
      var hardClose = false;

      var connexion = function connexion() {
        var url = "ws".concat(window.location.href.startsWith('https') ? 's' : '', "://").concat(_this5.props.baseUrl && _this5.props.baseUrl || window.location.host, "/").concat(_this5.state.page, "/ws");
        _this5.ws = new WebSocket(url);

        _this5.ws.addEventListener('message', _this5.onMessage);

        _this5.ws.onopen = function () {
          if (_this5.state.reloading) {
            hardClose = true;

            _this5.ws.close();

            if (_this5.state.needRefresh) {
              window.location.reload();
            } else {
              _this5.props.hotReload();
            }
          } else {
            _this5.setState({
              ready: true
            });

            tries = 0;
          }
        };

        _this5.ws.onclose = function () {
          var reconnect = function reconnect() {
            tries++;
            connexion();
          };

          if (!hardClose && tries < _this5.props.retries) {
            setTimeout(reconnect, 1000);
          }
        };
      };

      connexion();
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      var _this6 = this;

      this.pageApi('', {
        method: 'POST'
      }).then(function (response) {
        var toRegex = function toRegex(x) {
          return new RegExp(x);
        };

        _this6.setState({
          page: response.page,
          layout: response.layout,
          bindings: Object(ramda__WEBPACK_IMPORTED_MODULE_6__["pickBy"])(function (b) {
            return !b.regex;
          }, response.bindings),
          // Regex bindings triggers
          rebindings: Object(ramda__WEBPACK_IMPORTED_MODULE_6__["map"])(function (x) {
            var binding = response.bindings[x];
            binding.trigger = Object(ramda__WEBPACK_IMPORTED_MODULE_6__["evolve"])({
              identity: toRegex,
              aspect: toRegex
            }, binding.trigger);
            return binding;
          }, Object(ramda__WEBPACK_IMPORTED_MODULE_6__["keys"])(Object(ramda__WEBPACK_IMPORTED_MODULE_6__["pickBy"])(function (b) {
            return b.regex;
          }, response.bindings))),
          packages: response.packages,
          requirements: response.requirements
        }, function () {
          return Object(_requirements__WEBPACK_IMPORTED_MODULE_4__["loadRequirements"])(response.requirements, response.packages).then(function () {
            if (Object(ramda__WEBPACK_IMPORTED_MODULE_6__["keys"])(response.bindings).length || response.reload) {
              _this6._connectWS();
            } else {
              _this6.setState({
                ready: true
              });
            }
          });
        });
      });
    }
  }, {
    key: "render",
    value: function render() {
      var _this$state = this.state,
          layout = _this$state.layout,
          ready = _this$state.ready,
          reloading = _this$state.reloading;

      if (!ready) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          className: "dazzler-loading"
        }, "Loading...");
      }

      if (reloading) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          className: "dazzler-loading"
        }, "Reloading...");
      }

      if (!Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["isComponent"])(layout)) {
        throw new Error("Layout is not a component: ".concat(layout));
      }

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "dazzler-rendered"
      }, Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["hydrateComponent"])(layout.name, layout["package"], layout.identity, Object(_hydrator__WEBPACK_IMPORTED_MODULE_3__["hydrateProps"])(layout.aspects, this.updateAspects, this.connect, this.disconnect), this.updateAspects, this.connect, this.disconnect));
    }
  }]);

  return Updater;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Updater.defaultProps = {};
Updater.propTypes = {
  baseUrl: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  ping: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  ping_interval: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  retries: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  hotReload: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/renderer/js/components/Wrapper.jsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Wrapper.jsx ***!
  \************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Wrapper; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var commons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! commons */ "./src/commons/js/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * Wraps components for aspects updating.
 */

var Wrapper =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Wrapper, _React$Component);

  function Wrapper(props) {
    var _this;

    _classCallCheck(this, Wrapper);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Wrapper).call(this, props));
    _this.state = {
      aspects: props.aspects || {},
      ready: false,
      initial: false
    };
    _this.setAspects = _this.setAspects.bind(_assertThisInitialized(_this));
    _this.getAspect = _this.getAspect.bind(_assertThisInitialized(_this));
    _this.updateAspects = _this.updateAspects.bind(_assertThisInitialized(_this));
    _this.matchAspects = _this.matchAspects.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Wrapper, [{
    key: "updateAspects",
    value: function updateAspects(aspects) {
      var _this2 = this;

      return this.setAspects(aspects).then(function () {
        return _this2.props.updateAspects(_this2.props.identity, aspects);
      });
    }
  }, {
    key: "setAspects",
    value: function setAspects(aspects) {
      var _this3 = this;

      return new Promise(function (resolve) {
        _this3.setState({
          aspects: _objectSpread({}, _this3.state.aspects, aspects)
        }, resolve);
      });
    }
  }, {
    key: "getAspect",
    value: function getAspect(aspect) {
      return this.state.aspects[aspect];
    }
  }, {
    key: "matchAspects",
    value: function matchAspects(pattern) {
      var _this4 = this;

      return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["keys"])(this.state.aspects).filter(function (k) {
        return pattern.test(k);
      }).map(function (k) {
        return [k, _this4.state.aspects[k]];
      });
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      var _this5 = this;

      // Only update the component when mounted.
      // Otherwise gets a race condition with willUnmount
      this.props.connect(this.props.identity, this.setAspects, this.getAspect, this.matchAspects);

      if (!this.state.initial) {
        this.updateAspects(this.state.aspects).then(function () {
          return _this5.setState({
            ready: true,
            initial: true
          });
        });
      }
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      this.props.disconnect(this.props.identity);
    }
  }, {
    key: "render",
    value: function render() {
      var _this$props = this.props,
          component = _this$props.component,
          component_name = _this$props.component_name,
          package_name = _this$props.package_name;
      var _this$state = this.state,
          aspects = _this$state.aspects,
          ready = _this$state.ready;
      if (!ready) return null;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.cloneElement(component, _objectSpread({}, aspects, {
        updateAspects: this.updateAspects,
        identity: this.props.identity,
        class_name: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(["".concat(package_name.replace('_', '-').toLowerCase(), "-").concat(Object(commons__WEBPACK_IMPORTED_MODULE_3__["camelToSpinal"])(component_name))], aspects.class_name ? aspects.class_name.split(' ') : []))
      }));
    }
  }]);

  return Wrapper;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Wrapper.propTypes = {
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node.isRequired,
  connect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired,
  component_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  package_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  disconnect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func.isRequired
};

/***/ }),

/***/ "./src/renderer/js/hydrator.js":
/*!*************************************!*\
  !*** ./src/renderer/js/hydrator.js ***!
  \*************************************/
/*! exports provided: isComponent, hydrateProps, hydrateComponent, prepareProp */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isComponent", function() { return isComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "hydrateProps", function() { return hydrateProps; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "hydrateComponent", function() { return hydrateComponent; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "prepareProp", function() { return prepareProp; });
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Wrapper__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Wrapper */ "./src/renderer/js/components/Wrapper.jsx");
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance"); }

function _iterableToArrayLimit(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }




function isComponent(c) {
  return Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(c) === 'Object' && c.hasOwnProperty('package') && c.hasOwnProperty('aspects') && c.hasOwnProperty('name') && c.hasOwnProperty('identity');
}
function hydrateProps(props, updateAspects, connect, disconnect) {
  var replace = {};
  Object.entries(props).forEach(function (_ref) {
    var _ref2 = _slicedToArray(_ref, 2),
        k = _ref2[0],
        v = _ref2[1];

    if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(v) === 'Array') {
      replace[k] = v.map(function (c) {
        if (!isComponent(c)) {
          // Mixing components and primitives
          return c;
        }

        var newProps = hydrateProps(c.aspects, updateAspects, connect, disconnect);

        if (!newProps.key) {
          newProps.key = c.identity;
        }

        return hydrateComponent(c.name, c["package"], c.identity, newProps, updateAspects, connect, disconnect);
      });
    } else if (isComponent(v)) {
      var newProps = hydrateProps(v.aspects, updateAspects, connect, disconnect);
      replace[k] = hydrateComponent(v.name, v["package"], v.identity, newProps, updateAspects, connect, disconnect);
    } else if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(v) === 'Object') {
      replace[k] = hydrateProps(v, updateAspects, connect, disconnect);
    }
  });
  return _objectSpread({}, props, replace);
}
function hydrateComponent(name, package_name, identity, props, updateAspects, connect, disconnect) {
  var pack = window[package_name];
  var element = react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement(pack[name], props);
  return react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement(_components_Wrapper__WEBPACK_IMPORTED_MODULE_2__["default"], {
    identity: identity,
    updateAspects: updateAspects,
    component: element,
    connect: connect,
    package_name: package_name,
    component_name: name,
    aspects: props,
    disconnect: disconnect,
    key: "wrapper-".concat(identity)
  });
}
function prepareProp(prop) {
  if (react__WEBPACK_IMPORTED_MODULE_1___default.a.isValidElement(prop)) {
    return {
      identity: prop.props.identity,
      aspects: Object(ramda__WEBPACK_IMPORTED_MODULE_0__["map"])(prepareProp, Object(ramda__WEBPACK_IMPORTED_MODULE_0__["omit"])(['identity', 'updateAspects', '_name', '_package', 'aspects', 'key'], prop.props.aspects)),
      name: prop.props.component_name,
      "package": prop.props.package_name
    };
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(prop) === 'Array') {
    return prop.map(prepareProp);
  }

  if (Object(ramda__WEBPACK_IMPORTED_MODULE_0__["type"])(prop) === 'Object') {
    return Object(ramda__WEBPACK_IMPORTED_MODULE_0__["map"])(prepareProp, prop);
  }

  return prop;
}

/***/ }),

/***/ "./src/renderer/js/index.js":
/*!**********************************!*\
  !*** ./src/renderer/js/index.js ***!
  \**********************************/
/*! exports provided: Renderer, render */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dom */ "react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_Renderer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Renderer */ "./src/renderer/js/components/Renderer.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Renderer", function() { return _components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"]; });





function render(_ref, element) {
  var baseUrl = _ref.baseUrl,
      ping = _ref.ping,
      ping_interval = _ref.ping_interval,
      retries = _ref.retries;
  react_dom__WEBPACK_IMPORTED_MODULE_1___default.a.render(react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Renderer__WEBPACK_IMPORTED_MODULE_2__["default"], {
    baseUrl: baseUrl,
    ping: ping,
    ping_interval: ping_interval,
    retries: retries
  }), element);
}



/***/ }),

/***/ "./src/renderer/js/requests.js":
/*!*************************************!*\
  !*** ./src/renderer/js/requests.js ***!
  \*************************************/
/*! exports provided: JSONHEADERS, xhrRequest, apiRequest */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JSONHEADERS", function() { return JSONHEADERS; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "xhrRequest", function() { return xhrRequest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "apiRequest", function() { return apiRequest; });
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/* eslint-disable no-magic-numbers */
var jsonPattern = /json/i;
/**
 * @typedef {Object} XhrOptions
 * @property {string} [method='GET']
 * @property {Object} [headers={}]
 * @property {string|Blob|ArrayBuffer|object|Array} [payload='']
 */

/**
 * @type {XhrOptions}
 */

var defaultXhrOptions = {
  method: 'GET',
  headers: {},
  payload: '',
  json: true
};
var JSONHEADERS = {
  'Content-Type': 'application/json'
};
/**
 * Xhr promise wrap.
 *
 * Fetch can't do put request, so xhr still useful.
 *
 * Auto parse json responses.
 * Cancellation: xhr.abort
 * @param {string} url
 * @param {XhrOptions} [options]
 * @return {Promise}
 */

function xhrRequest(url) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : defaultXhrOptions;
  return new Promise(function (resolve, reject) {
    var _defaultXhrOptions$op = _objectSpread({}, defaultXhrOptions, options),
        method = _defaultXhrOptions$op.method,
        headers = _defaultXhrOptions$op.headers,
        payload = _defaultXhrOptions$op.payload,
        json = _defaultXhrOptions$op.json;

    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    var head = json ? _objectSpread({}, JSONHEADERS, headers) : headers;
    Object.keys(head).forEach(function (k) {
      return xhr.setRequestHeader(k, head[k]);
    });

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status < 400) {
          var responseValue = xhr.response;

          if (jsonPattern.test(xhr.getResponseHeader('Content-Type'))) {
            responseValue = JSON.parse(xhr.responseText);
          }

          resolve(responseValue);
        } else {
          reject({
            error: 'RequestError',
            message: "XHR ".concat(url, " FAILED - STATUS: ").concat(xhr.status, " MESSAGE: ").concat(xhr.statusText),
            status: xhr.status,
            xhr: xhr
          });
        }
      }
    };

    xhr.onerror = function (err) {
      return reject(err);
    };

    xhr.send(json ? JSON.stringify(payload) : payload);
  });
}
/**
 * Auto get headers and refresh/retry.
 *
 * @param {function} getHeaders
 * @param {function} refresh
 * @param {string} baseUrl
 */

function apiRequest() {
  var baseUrl = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
  return function () {
    var url = baseUrl + arguments[0];
    var options = arguments[1] || {};
    options.headers = _objectSpread({}, options.headers);
    return new Promise(function (resolve) {
      xhrRequest(url, options).then(resolve);
    });
  };
}

/***/ }),

/***/ "./src/renderer/js/requirements.js":
/*!*****************************************!*\
  !*** ./src/renderer/js/requirements.js ***!
  \*****************************************/
/*! exports provided: loadRequirement, loadRequirements */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "loadRequirement", function() { return loadRequirement; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "loadRequirements", function() { return loadRequirements; });
/* harmony import */ var commons__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! commons */ "./src/commons/js/index.js");

function loadRequirement(requirement) {
  return new Promise(function (resolve, reject) {
    var url = requirement.url,
        kind = requirement.kind,
        meta = requirement.meta;
    var method;

    if (kind === 'js') {
      method = commons__WEBPACK_IMPORTED_MODULE_0__["loadScript"];
    } else if (kind === 'css') {
      method = commons__WEBPACK_IMPORTED_MODULE_0__["loadCss"];
    } else if (kind === 'map') {
      return resolve();
    } else {
      return reject({
        error: "Invalid requirement kind: ".concat(kind)
      });
    }

    return method(url, meta).then(resolve)["catch"](reject);
  });
}
function loadRequirements(requirements, packages) {
  return new Promise(function (resolve, reject) {
    var loadings = []; // Load packages first.

    Object.keys(packages).forEach(function (pack_name) {
      var pack = packages[pack_name];
      loadings = loadings.concat(pack.requirements.map(loadRequirement));
    }); // Then load requirements so they can use packages
    // and override css.

    Promise.all(loadings).then(function () {
      var i = 0; // Load in order.

      var handler = function handler() {
        if (i < requirements.length) {
          loadRequirement(requirements[i]).then(function () {
            i++;
            handler();
          });
        } else {
          resolve();
        }
      };

      handler();
    })["catch"](reject);
  });
}

/***/ }),

/***/ 1:
/*!****************************************!*\
  !*** multi ./src/renderer/js/index.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/renderer/js/index.js */"./src/renderer/js/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************************************************!*\
  !*** external {"commonjs":"react-dom","commonjs2":"react-dom","amd":"react-dom","umd":"react-dom","root":"ReactDOM"} ***!
  \***********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1JlbmRlcmVyLmpzeD8iLCJ3ZWJwYWNrOi8vLy4vc3JjL3JlbmRlcmVyL2pzL2NvbXBvbmVudHMvVXBkYXRlci5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1dyYXBwZXIuanN4PyIsIndlYnBhY2s6Ly8vLi9zcmMvcmVuZGVyZXIvanMvaHlkcmF0b3IuanM/Iiwid2VicGFjazovLy8uL3NyYy9yZW5kZXJlci9qcy9pbmRleC5qcz8iLCJ3ZWJwYWNrOi8vLy4vc3JjL3JlbmRlcmVyL2pzL3JlcXVlc3RzLmpzPyIsIndlYnBhY2s6Ly8vLi9zcmMvcmVuZGVyZXIvanMvcmVxdWlyZW1lbnRzLmpzPyIsIndlYnBhY2s6Ly8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iLCJ3ZWJwYWNrOi8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdC1kb21cIixcImNvbW1vbmpzMlwiOlwicmVhY3QtZG9tXCIsXCJhbWRcIjpcInJlYWN0LWRvbVwiLFwidW1kXCI6XCJyZWFjdC1kb21cIixcInJvb3RcIjpcIlJlYWN0RE9NXCJ9PyJdLCJuYW1lcyI6WyJSZW5kZXJlciIsInByb3BzIiwidXNlU3RhdGUiLCJyZWxvYWRLZXkiLCJzZXRSZWxvYWRLZXkiLCJ3aW5kb3ciLCJkYXp6bGVyX2Jhc2VfdXJsIiwiYmFzZVVybCIsInByb3BUeXBlcyIsIlByb3BUeXBlcyIsInN0cmluZyIsImlzUmVxdWlyZWQiLCJwaW5nIiwiYm9vbCIsInBpbmdfaW50ZXJ2YWwiLCJudW1iZXIiLCJyZXRyaWVzIiwiVXBkYXRlciIsInN0YXRlIiwibGF5b3V0IiwicmVhZHkiLCJwYWdlIiwiYmluZGluZ3MiLCJwYWNrYWdlcyIsInJlcXVpcmVtZW50cyIsInJlbG9hZGluZyIsIm5lZWRSZWZyZXNoIiwicGFnZUFwaSIsImFwaVJlcXVlc3QiLCJsb2NhdGlvbiIsImhyZWYiLCJib3VuZENvbXBvbmVudHMiLCJ3cyIsInVwZGF0ZUFzcGVjdHMiLCJiaW5kIiwiY29ubmVjdCIsImRpc2Nvbm5lY3QiLCJvbk1lc3NhZ2UiLCJpZGVudGl0eSIsImFzcGVjdHMiLCJQcm9taXNlIiwicmVzb2x2ZSIsImFzcGVjdEtleXMiLCJrZXlzIiwibWFwIiwia2V5IiwidmFsdWUiLCJmaWx0ZXIiLCJlIiwidHJpZ2dlciIsInJlYmluZGluZ3MiLCJmb3JFYWNoIiwiYmluZGluZyIsInRlc3QiLCJjb25jYXQiLCJrIiwiYXNwZWN0IiwicHVzaCIsImNvbnNvbGUiLCJsb2ciLCJzZW5kQmluZGluZyIsImxlbmd0aCIsInNldEFzcGVjdHMiLCJnZXRBc3BlY3QiLCJtYXRjaEFzcGVjdHMiLCJyZXNwb25zZSIsImRhdGEiLCJKU09OIiwicGFyc2UiLCJraW5kIiwicGF5bG9hZCIsInN0b3JhZ2UiLCJyZXF1ZXN0X2lkIiwic3RvcmUiLCJzZXNzaW9uU3RvcmFnZSIsImxvY2FsU3RvcmFnZSIsImNvbXBvbmVudCIsImh5ZHJhdGVQcm9wcyIsInRoZW4iLCJyZWdleCIsInBhdHRlcm4iLCJSZWdFeHAiLCJ3YW50ZWQiLCJzZW5kIiwic3RyaW5naWZ5IiwiZXJyb3IiLCJwcmVwYXJlUHJvcCIsInNldEl0ZW0iLCJnZXRJdGVtIiwiZmlsZW5hbWVzIiwiaG90IiwicmVmcmVzaCIsImRlbGV0ZWQiLCJjbG9zZSIsInNldFN0YXRlIiwibG9hZFJlcXVpcmVtZW50IiwiciIsImRpc2FibGVDc3MiLCJ1cmwiLCJzdGF0ZXMiLCJyZWR1Y2UiLCJhY2MiLCJpZGVudGl0eVBhdHRlcm4iLCJhc3BlY3RQYXR0ZXJuIiwiZmxhdHRlbiIsInZhbHVlcyIsIm5hbWUiLCJ2YWwiLCJ0cmllcyIsImhhcmRDbG9zZSIsImNvbm5leGlvbiIsInN0YXJ0c1dpdGgiLCJob3N0IiwiV2ViU29ja2V0IiwiYWRkRXZlbnRMaXN0ZW5lciIsIm9ub3BlbiIsInJlbG9hZCIsImhvdFJlbG9hZCIsIm9uY2xvc2UiLCJyZWNvbm5lY3QiLCJzZXRUaW1lb3V0IiwibWV0aG9kIiwidG9SZWdleCIsIngiLCJwaWNrQnkiLCJiIiwiZXZvbHZlIiwibG9hZFJlcXVpcmVtZW50cyIsIl9jb25uZWN0V1MiLCJpc0NvbXBvbmVudCIsIkVycm9yIiwiaHlkcmF0ZUNvbXBvbmVudCIsIlJlYWN0IiwiQ29tcG9uZW50IiwiZGVmYXVsdFByb3BzIiwiZnVuYyIsIldyYXBwZXIiLCJpbml0aWFsIiwiY29tcG9uZW50X25hbWUiLCJwYWNrYWdlX25hbWUiLCJjbG9uZUVsZW1lbnQiLCJjbGFzc19uYW1lIiwiam9pbiIsInJlcGxhY2UiLCJ0b0xvd2VyQ2FzZSIsImNhbWVsVG9TcGluYWwiLCJzcGxpdCIsIm5vZGUiLCJjIiwidHlwZSIsImhhc093blByb3BlcnR5IiwiT2JqZWN0IiwiZW50cmllcyIsInYiLCJuZXdQcm9wcyIsInBhY2siLCJlbGVtZW50IiwiY3JlYXRlRWxlbWVudCIsInByb3AiLCJpc1ZhbGlkRWxlbWVudCIsIm9taXQiLCJyZW5kZXIiLCJSZWFjdERPTSIsImpzb25QYXR0ZXJuIiwiZGVmYXVsdFhock9wdGlvbnMiLCJoZWFkZXJzIiwianNvbiIsIkpTT05IRUFERVJTIiwieGhyUmVxdWVzdCIsIm9wdGlvbnMiLCJyZWplY3QiLCJ4aHIiLCJYTUxIdHRwUmVxdWVzdCIsIm9wZW4iLCJoZWFkIiwic2V0UmVxdWVzdEhlYWRlciIsIm9ucmVhZHlzdGF0ZWNoYW5nZSIsInJlYWR5U3RhdGUiLCJET05FIiwic3RhdHVzIiwicmVzcG9uc2VWYWx1ZSIsImdldFJlc3BvbnNlSGVhZGVyIiwicmVzcG9uc2VUZXh0IiwibWVzc2FnZSIsInN0YXR1c1RleHQiLCJvbmVycm9yIiwiZXJyIiwiYXJndW1lbnRzIiwicmVxdWlyZW1lbnQiLCJtZXRhIiwibG9hZFNjcmlwdCIsImxvYWRDc3MiLCJsb2FkaW5ncyIsInBhY2tfbmFtZSIsImFsbCIsImkiLCJoYW5kbGVyIl0sIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTztBQ1ZBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0JBQVEsb0JBQW9CO0FBQzVCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EseUJBQWlCLDRCQUE0QjtBQUM3QztBQUNBO0FBQ0EsMEJBQWtCLDJCQUEyQjtBQUM3QztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOzs7QUFHQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0Esa0RBQTBDLGdDQUFnQztBQUMxRTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGdFQUF3RCxrQkFBa0I7QUFDMUU7QUFDQSx5REFBaUQsY0FBYztBQUMvRDs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaURBQXlDLGlDQUFpQztBQUMxRSx3SEFBZ0gsbUJBQW1CLEVBQUU7QUFDckk7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxtQ0FBMkIsMEJBQTBCLEVBQUU7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QjtBQUNwQyxRQUFJc0IsUUFBUSxHQUFHLEVBQWYsQ0FEb0MsQ0FFcEM7O0FBQ0F6QyxVQUFNLENBQUM1RyxJQUFQLENBQVlwQixRQUFaLEVBQXNCNEIsT0FBdEIsQ0FBOEIsVUFBQThJLFNBQVMsRUFBSTtBQUN2QyxVQUFNdEMsSUFBSSxHQUFHcEksUUFBUSxDQUFDMEssU0FBRCxDQUFyQjtBQUNBRCxjQUFRLEdBQUdBLFFBQVEsQ0FBQzFJLE1BQVQsQ0FBZ0JxRyxJQUFJLENBQUNuSSxZQUFMLENBQWtCb0IsR0FBbEIsQ0FBc0JtRCxlQUF0QixDQUFoQixDQUFYO0FBQ0gsS0FIRCxFQUhvQyxDQU9wQztBQUNBOztBQUNBdkQsV0FBTyxDQUFDMEosR0FBUixDQUFZRixRQUFaLEVBQ0tsSCxJQURMLENBQ1UsWUFBTTtBQUNSLFVBQUlxSCxDQUFDLEdBQUcsQ0FBUixDQURRLENBRVI7O0FBQ0EsVUFBTUMsT0FBTyxHQUFHLFNBQVZBLE9BQVUsR0FBTTtBQUNsQixZQUFJRCxDQUFDLEdBQUczSyxZQUFZLENBQUNxQyxNQUFyQixFQUE2QjtBQUN6QmtDLHlCQUFlLENBQUN2RSxZQUFZLENBQUMySyxDQUFELENBQWIsQ0FBZixDQUFpQ3JILElBQWpDLENBQXNDLFlBQU07QUFDeENxSCxhQUFDO0FBQ0RDLG1CQUFPO0FBQ1YsV0FIRDtBQUlILFNBTEQsTUFLTztBQUNIM0osaUJBQU87QUFDVjtBQUNKLE9BVEQ7O0FBVUEySixhQUFPO0FBQ1YsS0FmTCxXQWdCVzFCLE1BaEJYO0FBaUJILEdBMUJNLENBQVA7QUEyQkgsQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNqREQsbUQ7Ozs7Ozs7Ozs7O0FDQUEsdUQiLCJmaWxlIjoiZGF6emxlcl9yZW5kZXJlcl8zOTViNDFlZmI0YzA5ZjI1YjljNy5qcyIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpLCByZXF1aXJlKFwicmVhY3QtZG9tXCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCIsIFwicmVhY3QtZG9tXCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfcmVuZGVyZXJcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSwgcmVxdWlyZShcInJlYWN0LWRvbVwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9yZW5kZXJlclwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdLCByb290W1wiUmVhY3RET01cIl0pO1xufSkod2luZG93LCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18sIF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfZG9tX18pIHtcbnJldHVybiAiLCIgXHQvLyBpbnN0YWxsIGEgSlNPTlAgY2FsbGJhY2sgZm9yIGNodW5rIGxvYWRpbmdcbiBcdGZ1bmN0aW9uIHdlYnBhY2tKc29ucENhbGxiYWNrKGRhdGEpIHtcbiBcdFx0dmFyIGNodW5rSWRzID0gZGF0YVswXTtcbiBcdFx0dmFyIG1vcmVNb2R1bGVzID0gZGF0YVsxXTtcbiBcdFx0dmFyIGV4ZWN1dGVNb2R1bGVzID0gZGF0YVsyXTtcblxuIFx0XHQvLyBhZGQgXCJtb3JlTW9kdWxlc1wiIHRvIHRoZSBtb2R1bGVzIG9iamVjdCxcbiBcdFx0Ly8gdGhlbiBmbGFnIGFsbCBcImNodW5rSWRzXCIgYXMgbG9hZGVkIGFuZCBmaXJlIGNhbGxiYWNrXG4gXHRcdHZhciBtb2R1bGVJZCwgY2h1bmtJZCwgaSA9IDAsIHJlc29sdmVzID0gW107XG4gXHRcdGZvcig7aSA8IGNodW5rSWRzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0Y2h1bmtJZCA9IGNodW5rSWRzW2ldO1xuIFx0XHRcdGlmKGluc3RhbGxlZENodW5rc1tjaHVua0lkXSkge1xuIFx0XHRcdFx0cmVzb2x2ZXMucHVzaChpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF1bMF0pO1xuIFx0XHRcdH1cbiBcdFx0XHRpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF0gPSAwO1xuIFx0XHR9XG4gXHRcdGZvcihtb2R1bGVJZCBpbiBtb3JlTW9kdWxlcykge1xuIFx0XHRcdGlmKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChtb3JlTW9kdWxlcywgbW9kdWxlSWQpKSB7XG4gXHRcdFx0XHRtb2R1bGVzW21vZHVsZUlkXSA9IG1vcmVNb2R1bGVzW21vZHVsZUlkXTtcbiBcdFx0XHR9XG4gXHRcdH1cbiBcdFx0aWYocGFyZW50SnNvbnBGdW5jdGlvbikgcGFyZW50SnNvbnBGdW5jdGlvbihkYXRhKTtcblxuIFx0XHR3aGlsZShyZXNvbHZlcy5sZW5ndGgpIHtcbiBcdFx0XHRyZXNvbHZlcy5zaGlmdCgpKCk7XG4gXHRcdH1cblxuIFx0XHQvLyBhZGQgZW50cnkgbW9kdWxlcyBmcm9tIGxvYWRlZCBjaHVuayB0byBkZWZlcnJlZCBsaXN0XG4gXHRcdGRlZmVycmVkTW9kdWxlcy5wdXNoLmFwcGx5KGRlZmVycmVkTW9kdWxlcywgZXhlY3V0ZU1vZHVsZXMgfHwgW10pO1xuXG4gXHRcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gYWxsIGNodW5rcyByZWFkeVxuIFx0XHRyZXR1cm4gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKTtcbiBcdH07XG4gXHRmdW5jdGlvbiBjaGVja0RlZmVycmVkTW9kdWxlcygpIHtcbiBcdFx0dmFyIHJlc3VsdDtcbiBcdFx0Zm9yKHZhciBpID0gMDsgaSA8IGRlZmVycmVkTW9kdWxlcy5sZW5ndGg7IGkrKykge1xuIFx0XHRcdHZhciBkZWZlcnJlZE1vZHVsZSA9IGRlZmVycmVkTW9kdWxlc1tpXTtcbiBcdFx0XHR2YXIgZnVsZmlsbGVkID0gdHJ1ZTtcbiBcdFx0XHRmb3IodmFyIGogPSAxOyBqIDwgZGVmZXJyZWRNb2R1bGUubGVuZ3RoOyBqKyspIHtcbiBcdFx0XHRcdHZhciBkZXBJZCA9IGRlZmVycmVkTW9kdWxlW2pdO1xuIFx0XHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2RlcElkXSAhPT0gMCkgZnVsZmlsbGVkID0gZmFsc2U7XG4gXHRcdFx0fVxuIFx0XHRcdGlmKGZ1bGZpbGxlZCkge1xuIFx0XHRcdFx0ZGVmZXJyZWRNb2R1bGVzLnNwbGljZShpLS0sIDEpO1xuIFx0XHRcdFx0cmVzdWx0ID0gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSBkZWZlcnJlZE1vZHVsZVswXSk7XG4gXHRcdFx0fVxuIFx0XHR9XG5cbiBcdFx0cmV0dXJuIHJlc3VsdDtcbiBcdH1cblxuIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gb2JqZWN0IHRvIHN0b3JlIGxvYWRlZCBhbmQgbG9hZGluZyBjaHVua3NcbiBcdC8vIHVuZGVmaW5lZCA9IGNodW5rIG5vdCBsb2FkZWQsIG51bGwgPSBjaHVuayBwcmVsb2FkZWQvcHJlZmV0Y2hlZFxuIFx0Ly8gUHJvbWlzZSA9IGNodW5rIGxvYWRpbmcsIDAgPSBjaHVuayBsb2FkZWRcbiBcdHZhciBpbnN0YWxsZWRDaHVua3MgPSB7XG4gXHRcdFwicmVuZGVyZXJcIjogMFxuIFx0fTtcblxuIFx0dmFyIGRlZmVycmVkTW9kdWxlcyA9IFtdO1xuXG4gXHQvLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuIFx0ZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXG4gXHRcdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuIFx0XHRpZihpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSkge1xuIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuIFx0XHR9XG4gXHRcdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG4gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbiBcdFx0XHRpOiBtb2R1bGVJZCxcbiBcdFx0XHRsOiBmYWxzZSxcbiBcdFx0XHRleHBvcnRzOiB7fVxuIFx0XHR9O1xuXG4gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuIFx0XHRtb2R1bGVzW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4gXHRcdG1vZHVsZS5sID0gdHJ1ZTtcblxuIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuIFx0XHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG4gXHR9XG5cblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlIGNhY2hlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuXG4gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uZCA9IGZ1bmN0aW9uKGV4cG9ydHMsIG5hbWUsIGdldHRlcikge1xuIFx0XHRpZighX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIG5hbWUpKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHsgZW51bWVyYWJsZTogdHJ1ZSwgZ2V0OiBnZXR0ZXIgfSk7XG4gXHRcdH1cbiBcdH07XG5cbiBcdC8vIGRlZmluZSBfX2VzTW9kdWxlIG9uIGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uciA9IGZ1bmN0aW9uKGV4cG9ydHMpIHtcbiBcdFx0aWYodHlwZW9mIFN5bWJvbCAhPT0gJ3VuZGVmaW5lZCcgJiYgU3ltYm9sLnRvU3RyaW5nVGFnKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFN5bWJvbC50b1N0cmluZ1RhZywgeyB2YWx1ZTogJ01vZHVsZScgfSk7XG4gXHRcdH1cbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsICdfX2VzTW9kdWxlJywgeyB2YWx1ZTogdHJ1ZSB9KTtcbiBcdH07XG5cbiBcdC8vIGNyZWF0ZSBhIGZha2UgbmFtZXNwYWNlIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDE6IHZhbHVlIGlzIGEgbW9kdWxlIGlkLCByZXF1aXJlIGl0XG4gXHQvLyBtb2RlICYgMjogbWVyZ2UgYWxsIHByb3BlcnRpZXMgb2YgdmFsdWUgaW50byB0aGUgbnNcbiBcdC8vIG1vZGUgJiA0OiByZXR1cm4gdmFsdWUgd2hlbiBhbHJlYWR5IG5zIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDh8MTogYmVoYXZlIGxpa2UgcmVxdWlyZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy50ID0gZnVuY3Rpb24odmFsdWUsIG1vZGUpIHtcbiBcdFx0aWYobW9kZSAmIDEpIHZhbHVlID0gX193ZWJwYWNrX3JlcXVpcmVfXyh2YWx1ZSk7XG4gXHRcdGlmKG1vZGUgJiA4KSByZXR1cm4gdmFsdWU7XG4gXHRcdGlmKChtb2RlICYgNCkgJiYgdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB2YWx1ZSAmJiB2YWx1ZS5fX2VzTW9kdWxlKSByZXR1cm4gdmFsdWU7XG4gXHRcdHZhciBucyA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18ucihucyk7XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShucywgJ2RlZmF1bHQnLCB7IGVudW1lcmFibGU6IHRydWUsIHZhbHVlOiB2YWx1ZSB9KTtcbiBcdFx0aWYobW9kZSAmIDIgJiYgdHlwZW9mIHZhbHVlICE9ICdzdHJpbmcnKSBmb3IodmFyIGtleSBpbiB2YWx1ZSkgX193ZWJwYWNrX3JlcXVpcmVfXy5kKG5zLCBrZXksIGZ1bmN0aW9uKGtleSkgeyByZXR1cm4gdmFsdWVba2V5XTsgfS5iaW5kKG51bGwsIGtleSkpO1xuIFx0XHRyZXR1cm4gbnM7XG4gXHR9O1xuXG4gXHQvLyBnZXREZWZhdWx0RXhwb3J0IGZ1bmN0aW9uIGZvciBjb21wYXRpYmlsaXR5IHdpdGggbm9uLWhhcm1vbnkgbW9kdWxlc1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5uID0gZnVuY3Rpb24obW9kdWxlKSB7XG4gXHRcdHZhciBnZXR0ZXIgPSBtb2R1bGUgJiYgbW9kdWxlLl9fZXNNb2R1bGUgP1xuIFx0XHRcdGZ1bmN0aW9uIGdldERlZmF1bHQoKSB7IHJldHVybiBtb2R1bGVbJ2RlZmF1bHQnXTsgfSA6XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0TW9kdWxlRXhwb3J0cygpIHsgcmV0dXJuIG1vZHVsZTsgfTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kKGdldHRlciwgJ2EnLCBnZXR0ZXIpO1xuIFx0XHRyZXR1cm4gZ2V0dGVyO1xuIFx0fTtcblxuIFx0Ly8gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm8gPSBmdW5jdGlvbihvYmplY3QsIHByb3BlcnR5KSB7IHJldHVybiBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqZWN0LCBwcm9wZXJ0eSk7IH07XG5cbiBcdC8vIF9fd2VicGFja19wdWJsaWNfcGF0aF9fXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnAgPSBcIlwiO1xuXG4gXHR2YXIganNvbnBBcnJheSA9IHdpbmRvd1tcIndlYnBhY2tKc29ucGRhenpsZXJfbmFtZV9cIl0gPSB3aW5kb3dbXCJ3ZWJwYWNrSnNvbnBkYXp6bGVyX25hbWVfXCJdIHx8IFtdO1xuIFx0dmFyIG9sZEpzb25wRnVuY3Rpb24gPSBqc29ucEFycmF5LnB1c2guYmluZChqc29ucEFycmF5KTtcbiBcdGpzb25wQXJyYXkucHVzaCA9IHdlYnBhY2tKc29ucENhbGxiYWNrO1xuIFx0anNvbnBBcnJheSA9IGpzb25wQXJyYXkuc2xpY2UoKTtcbiBcdGZvcih2YXIgaSA9IDA7IGkgPCBqc29ucEFycmF5Lmxlbmd0aDsgaSsrKSB3ZWJwYWNrSnNvbnBDYWxsYmFjayhqc29ucEFycmF5W2ldKTtcbiBcdHZhciBwYXJlbnRKc29ucEZ1bmN0aW9uID0gb2xkSnNvbnBGdW5jdGlvbjtcblxuXG4gXHQvLyBhZGQgZW50cnkgbW9kdWxlIHRvIGRlZmVycmVkIGxpc3RcbiBcdGRlZmVycmVkTW9kdWxlcy5wdXNoKFsxLFwiY29tbW9uc1wiXSk7XG4gXHQvLyBydW4gZGVmZXJyZWQgbW9kdWxlcyB3aGVuIHJlYWR5XG4gXHRyZXR1cm4gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKTtcbiIsImltcG9ydCBSZWFjdCwge3VzZVN0YXRlfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgVXBkYXRlciBmcm9tICcuL1VwZGF0ZXInO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuY29uc3QgUmVuZGVyZXIgPSBwcm9wcyA9PiB7XG4gICAgY29uc3QgW3JlbG9hZEtleSwgc2V0UmVsb2FkS2V5XSA9IHVzZVN0YXRlKDEpO1xuXG4gICAgLy8gRklYTUUgZmluZCB3aGVyZSB0aGlzIGlzIHVzZWQgYW5kIHJlZmFjdG9yL3JlbW92ZVxuICAgIHdpbmRvdy5kYXp6bGVyX2Jhc2VfdXJsID0gcHJvcHMuYmFzZVVybDtcbiAgICByZXR1cm4gKFxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRhenpsZXItcmVuZGVyZXJcIj5cbiAgICAgICAgICAgIDxVcGRhdGVyXG4gICAgICAgICAgICAgICAgey4uLnByb3BzfVxuICAgICAgICAgICAgICAgIGtleT17YHVwZC0ke3JlbG9hZEtleX1gfVxuICAgICAgICAgICAgICAgIGhvdFJlbG9hZD17KCkgPT4gc2V0UmVsb2FkS2V5KHJlbG9hZEtleSArIDEpfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgPC9kaXY+XG4gICAgKTtcbn07XG5cblJlbmRlcmVyLnByb3BUeXBlcyA9IHtcbiAgICBiYXNlVXJsOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgcGluZzogUHJvcFR5cGVzLmJvb2wsXG4gICAgcGluZ19pbnRlcnZhbDogUHJvcFR5cGVzLm51bWJlcixcbiAgICByZXRyaWVzOiBQcm9wVHlwZXMubnVtYmVyLFxufTtcblxuZXhwb3J0IGRlZmF1bHQgUmVuZGVyZXI7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7YXBpUmVxdWVzdH0gZnJvbSAnLi4vcmVxdWVzdHMnO1xuaW1wb3J0IHtcbiAgICBoeWRyYXRlQ29tcG9uZW50LFxuICAgIGh5ZHJhdGVQcm9wcyxcbiAgICBpc0NvbXBvbmVudCxcbiAgICBwcmVwYXJlUHJvcCxcbn0gZnJvbSAnLi4vaHlkcmF0b3InO1xuaW1wb3J0IHtsb2FkUmVxdWlyZW1lbnQsIGxvYWRSZXF1aXJlbWVudHN9IGZyb20gJy4uL3JlcXVpcmVtZW50cyc7XG5pbXBvcnQge2Rpc2FibGVDc3N9IGZyb20gJ2NvbW1vbnMnO1xuaW1wb3J0IHtwaWNrQnksIGtleXMsIG1hcCwgZXZvbHZlLCBjb25jYXQsIGZsYXR0ZW59IGZyb20gJ3JhbWRhJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVXBkYXRlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgbGF5b3V0OiBmYWxzZSxcbiAgICAgICAgICAgIHJlYWR5OiBmYWxzZSxcbiAgICAgICAgICAgIHBhZ2U6IG51bGwsXG4gICAgICAgICAgICBiaW5kaW5nczoge30sXG4gICAgICAgICAgICBwYWNrYWdlczogW10sXG4gICAgICAgICAgICByZXF1aXJlbWVudHM6IFtdLFxuICAgICAgICAgICAgcmVsb2FkaW5nOiBmYWxzZSxcbiAgICAgICAgICAgIG5lZWRSZWZyZXNoOiBmYWxzZSxcbiAgICAgICAgfTtcbiAgICAgICAgLy8gVGhlIGFwaSB1cmwgZm9yIHRoZSBwYWdlIGlzIHRoZSBzYW1lIGJ1dCBhIHBvc3QuXG4gICAgICAgIC8vIEZldGNoIGJpbmRpbmdzLCBwYWNrYWdlcyAmIHJlcXVpcmVtZW50c1xuICAgICAgICB0aGlzLnBhZ2VBcGkgPSBhcGlSZXF1ZXN0KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgICAgLy8gQWxsIGNvbXBvbmVudHMgZ2V0IGNvbm5lY3RlZC5cbiAgICAgICAgdGhpcy5ib3VuZENvbXBvbmVudHMgPSB7fTtcbiAgICAgICAgdGhpcy53cyA9IG51bGw7XG5cbiAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzID0gdGhpcy51cGRhdGVBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMuY29ubmVjdCA9IHRoaXMuY29ubmVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmRpc2Nvbm5lY3QgPSB0aGlzLmRpc2Nvbm5lY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5vbk1lc3NhZ2UgPSB0aGlzLm9uTWVzc2FnZS5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHVwZGF0ZUFzcGVjdHMoaWRlbnRpdHksIGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKHJlc29sdmUgPT4ge1xuICAgICAgICAgICAgY29uc3QgYXNwZWN0S2V5cyA9IGtleXMoYXNwZWN0cyk7XG4gICAgICAgICAgICBsZXQgYmluZGluZ3MgPSBhc3BlY3RLZXlzXG4gICAgICAgICAgICAgICAgLm1hcChrZXkgPT4gKHtcbiAgICAgICAgICAgICAgICAgICAgLi4udGhpcy5zdGF0ZS5iaW5kaW5nc1tgJHtrZXl9QCR7aWRlbnRpdHl9YF0sXG4gICAgICAgICAgICAgICAgICAgIHZhbHVlOiBhc3BlY3RzW2tleV0sXG4gICAgICAgICAgICAgICAgfSkpXG4gICAgICAgICAgICAgICAgLmZpbHRlcihlID0+IGUudHJpZ2dlcik7XG5cbiAgICAgICAgICAgIHRoaXMuc3RhdGUucmViaW5kaW5ncy5mb3JFYWNoKGJpbmRpbmcgPT4ge1xuICAgICAgICAgICAgICAgIGlmIChiaW5kaW5nLnRyaWdnZXIuaWRlbnRpdHkudGVzdChpZGVudGl0eSkpIHtcbiAgICAgICAgICAgICAgICAgICAgYmluZGluZ3MgPSBjb25jYXQoXG4gICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5ncyxcbiAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdEtleXNcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAuZmlsdGVyKGsgPT4gYmluZGluZy50cmlnZ2VyLmFzcGVjdC50ZXN0KGspKVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5tYXAoayA9PiAoe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAuLi5iaW5kaW5nLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogYXNwZWN0c1trXSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdHJpZ2dlcjoge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLi4uYmluZGluZy50cmlnZ2VyLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhc3BlY3Q6IGssXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgfSkpXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzLnB1c2goKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KTtcblxuICAgICAgICAgICAgaWYgKCFiaW5kaW5ncykge1xuICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKCdiaW5kaW5nJyk7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHJlc29sdmUoMCk7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIGJpbmRpbmdzLmZvckVhY2goYmluZGluZyA9PlxuICAgICAgICAgICAgICAgIHRoaXMuc2VuZEJpbmRpbmcoYmluZGluZywgYmluZGluZy52YWx1ZSlcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICByZXNvbHZlKGJpbmRpbmdzLmxlbmd0aCk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGNvbm5lY3QoaWRlbnRpdHksIHNldEFzcGVjdHMsIGdldEFzcGVjdCwgbWF0Y2hBc3BlY3RzKSB7XG4gICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW2lkZW50aXR5XSA9IHtcbiAgICAgICAgICAgIHNldEFzcGVjdHMsXG4gICAgICAgICAgICBnZXRBc3BlY3QsXG4gICAgICAgICAgICBtYXRjaEFzcGVjdHMsXG4gICAgICAgIH07XG4gICAgfVxuXG4gICAgZGlzY29ubmVjdChpZGVudGl0eSkge1xuICAgICAgICBkZWxldGUgdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgIH1cblxuICAgIG9uTWVzc2FnZShyZXNwb25zZSkge1xuICAgICAgICBjb25zdCBkYXRhID0gSlNPTi5wYXJzZShyZXNwb25zZS5kYXRhKTtcbiAgICAgICAgY29uc3Qge2lkZW50aXR5LCBraW5kLCBwYXlsb2FkLCBzdG9yYWdlLCByZXF1ZXN0X2lkfSA9IGRhdGE7XG4gICAgICAgIGxldCBzdG9yZTtcbiAgICAgICAgaWYgKHN0b3JhZ2UgPT09ICdzZXNzaW9uJykge1xuICAgICAgICAgICAgc3RvcmUgPSB3aW5kb3cuc2Vzc2lvblN0b3JhZ2U7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBzdG9yZSA9IHdpbmRvdy5sb2NhbFN0b3JhZ2U7XG4gICAgICAgIH1cbiAgICAgICAgc3dpdGNoIChraW5kKSB7XG4gICAgICAgICAgICBjYXNlICdzZXQtYXNwZWN0JzpcbiAgICAgICAgICAgICAgICBjb25zdCBzZXRBc3BlY3RzID0gY29tcG9uZW50ID0+XG4gICAgICAgICAgICAgICAgICAgIGNvbXBvbmVudFxuICAgICAgICAgICAgICAgICAgICAgICAgLnNldEFzcGVjdHMoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYXlsb2FkLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5kaXNjb25uZWN0XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICAgICAgLnRoZW4oKCkgPT4gdGhpcy51cGRhdGVBc3BlY3RzKGlkZW50aXR5LCBwYXlsb2FkKSk7XG4gICAgICAgICAgICAgICAgaWYgKGRhdGEucmVnZXgpIHtcbiAgICAgICAgICAgICAgICAgICAgY29uc3QgcGF0dGVybiA9IG5ldyBSZWdFeHAoZGF0YS5pZGVudGl0eSk7XG4gICAgICAgICAgICAgICAgICAgIGtleXModGhpcy5ib3VuZENvbXBvbmVudHMpXG4gICAgICAgICAgICAgICAgICAgICAgICAuZmlsdGVyKGsgPT4gcGF0dGVybi50ZXN0KGspKVxuICAgICAgICAgICAgICAgICAgICAgICAgLm1hcChrID0+IHRoaXMuYm91bmRDb21wb25lbnRzW2tdKVxuICAgICAgICAgICAgICAgICAgICAgICAgLmZvckVhY2goc2V0QXNwZWN0cyk7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgc2V0QXNwZWN0cyh0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV0pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ2dldC1hc3BlY3QnOlxuICAgICAgICAgICAgICAgIGNvbnN0IHthc3BlY3R9ID0gZGF0YTtcbiAgICAgICAgICAgICAgICBjb25zdCB3YW50ZWQgPSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgICAgICAgICAgICAgaWYgKCF3YW50ZWQpIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy53cy5zZW5kKFxuICAgICAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGtpbmQsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3RfaWQsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3I6IGBBc3BlY3Qgbm90IGZvdW5kICR7aWRlbnRpdHl9LiR7YXNwZWN0fWAsXG4gICAgICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGNvbnN0IHZhbHVlID0gd2FudGVkLmdldEFzcGVjdChhc3BlY3QpO1xuICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAga2luZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0LFxuICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU6IHByZXBhcmVQcm9wKHZhbHVlKSxcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3RfaWQsXG4gICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ3NldC1zdG9yYWdlJzpcbiAgICAgICAgICAgICAgICBzdG9yZS5zZXRJdGVtKGlkZW50aXR5LCBKU09OLnN0cmluZ2lmeShwYXlsb2FkKSk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdnZXQtc3RvcmFnZSc6XG4gICAgICAgICAgICAgICAgdGhpcy53cy5zZW5kKFxuICAgICAgICAgICAgICAgICAgICBKU09OLnN0cmluZ2lmeSh7XG4gICAgICAgICAgICAgICAgICAgICAgICBraW5kLFxuICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU6IEpTT04ucGFyc2Uoc3RvcmUuZ2V0SXRlbShpZGVudGl0eSkpLFxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdyZWxvYWQnOlxuICAgICAgICAgICAgICAgIGNvbnN0IHtmaWxlbmFtZXMsIGhvdCwgcmVmcmVzaCwgZGVsZXRlZH0gPSBkYXRhO1xuICAgICAgICAgICAgICAgIGlmIChyZWZyZXNoKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3MuY2xvc2UoKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHRoaXMuc2V0U3RhdGUoe3JlbG9hZGluZzogdHJ1ZSwgbmVlZFJlZnJlc2g6IHRydWV9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgaWYgKGhvdCkge1xuICAgICAgICAgICAgICAgICAgICAvLyBUaGUgd3MgY29ubmVjdGlvbiB3aWxsIGNsb3NlLCB3aGVuIGl0XG4gICAgICAgICAgICAgICAgICAgIC8vIHJlY29ubmVjdCBpdCB3aWxsIGRvIGEgaGFyZCByZWxvYWQgb2YgdGhlIHBhZ2UgYXBpLlxuICAgICAgICAgICAgICAgICAgICByZXR1cm4gdGhpcy5zZXRTdGF0ZSh7cmVsb2FkaW5nOiB0cnVlfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGZpbGVuYW1lcy5mb3JFYWNoKGxvYWRSZXF1aXJlbWVudCk7XG4gICAgICAgICAgICAgICAgZGVsZXRlZC5mb3JFYWNoKHIgPT4gZGlzYWJsZUNzcyhyLnVybCkpO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAncGluZyc6XG4gICAgICAgICAgICAgICAgLy8gSnVzdCBkbyBub3RoaW5nLlxuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgc2VuZEJpbmRpbmcoYmluZGluZywgdmFsdWUpIHtcbiAgICAgICAgLy8gQ29sbGVjdCBhbGwgdmFsdWVzIGFuZCBzZW5kIGEgYmluZGluZyBwYXlsb2FkXG4gICAgICAgIGNvbnN0IHRyaWdnZXIgPSB7XG4gICAgICAgICAgICAuLi5iaW5kaW5nLnRyaWdnZXIsXG4gICAgICAgICAgICB2YWx1ZTogcHJlcGFyZVByb3AodmFsdWUpLFxuICAgICAgICB9O1xuICAgICAgICBjb25zdCBzdGF0ZXMgPSBiaW5kaW5nLnN0YXRlcy5yZWR1Y2UoKGFjYywgc3RhdGUpID0+IHtcbiAgICAgICAgICAgIGlmIChzdGF0ZS5yZWdleCkge1xuICAgICAgICAgICAgICAgIGNvbnN0IGlkZW50aXR5UGF0dGVybiA9IG5ldyBSZWdFeHAoc3RhdGUuaWRlbnRpdHkpO1xuICAgICAgICAgICAgICAgIGNvbnN0IGFzcGVjdFBhdHRlcm4gPSBuZXcgUmVnRXhwKHN0YXRlLmFzcGVjdCk7XG4gICAgICAgICAgICAgICAgcmV0dXJuIGNvbmNhdChcbiAgICAgICAgICAgICAgICAgICAgYWNjLFxuICAgICAgICAgICAgICAgICAgICBmbGF0dGVuKFxuICAgICAgICAgICAgICAgICAgICAgICAga2V5cyh0aGlzLmJvdW5kQ29tcG9uZW50cykubWFwKGsgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxldCB2YWx1ZXMgPSBbXTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoaWRlbnRpdHlQYXR0ZXJuLnRlc3QoaykpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWVzID0gdGhpcy5ib3VuZENvbXBvbmVudHNba11cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5tYXRjaEFzcGVjdHMoYXNwZWN0UGF0dGVybilcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5tYXAoKFtuYW1lLCB2YWxdKSA9PiAoe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLnN0YXRlLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5OiBrLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdDogbmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogcHJlcGFyZVByb3AodmFsKSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pKTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHZhbHVlcztcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBhY2MucHVzaCh7XG4gICAgICAgICAgICAgICAgLi4uc3RhdGUsXG4gICAgICAgICAgICAgICAgdmFsdWU6XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XSAmJlxuICAgICAgICAgICAgICAgICAgICBwcmVwYXJlUHJvcChcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XS5nZXRBc3BlY3QoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgc3RhdGUuYXNwZWN0XG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIHJldHVybiBhY2M7XG4gICAgICAgIH0sIFtdKTtcblxuICAgICAgICBjb25zdCBwYXlsb2FkID0ge1xuICAgICAgICAgICAgdHJpZ2dlcixcbiAgICAgICAgICAgIHN0YXRlcyxcbiAgICAgICAgICAgIGtpbmQ6ICdiaW5kaW5nJyxcbiAgICAgICAgICAgIHBhZ2U6IHRoaXMuc3RhdGUucGFnZSxcbiAgICAgICAgICAgIGtleTogYmluZGluZy5rZXksXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMud3Muc2VuZChKU09OLnN0cmluZ2lmeShwYXlsb2FkKSk7XG4gICAgfVxuXG4gICAgX2Nvbm5lY3RXUygpIHtcbiAgICAgICAgLy8gU2V0dXAgd2Vic29ja2V0IGZvciB1cGRhdGVzXG4gICAgICAgIGxldCB0cmllcyA9IDA7XG4gICAgICAgIGxldCBoYXJkQ2xvc2UgPSBmYWxzZTtcbiAgICAgICAgY29uc3QgY29ubmV4aW9uID0gKCkgPT4ge1xuICAgICAgICAgICAgY29uc3QgdXJsID0gYHdzJHtcbiAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24uaHJlZi5zdGFydHNXaXRoKCdodHRwcycpID8gJ3MnIDogJydcbiAgICAgICAgICAgIH06Ly8keyh0aGlzLnByb3BzLmJhc2VVcmwgJiYgdGhpcy5wcm9wcy5iYXNlVXJsKSB8fFxuICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5ob3N0fS8ke3RoaXMuc3RhdGUucGFnZX0vd3NgO1xuICAgICAgICAgICAgdGhpcy53cyA9IG5ldyBXZWJTb2NrZXQodXJsKTtcbiAgICAgICAgICAgIHRoaXMud3MuYWRkRXZlbnRMaXN0ZW5lcignbWVzc2FnZScsIHRoaXMub25NZXNzYWdlKTtcbiAgICAgICAgICAgIHRoaXMud3Mub25vcGVuID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgIGlmICh0aGlzLnN0YXRlLnJlbG9hZGluZykge1xuICAgICAgICAgICAgICAgICAgICBoYXJkQ2xvc2UgPSB0cnVlO1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLmNsb3NlKCk7XG4gICAgICAgICAgICAgICAgICAgIGlmICh0aGlzLnN0YXRlLm5lZWRSZWZyZXNoKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24ucmVsb2FkKCk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnByb3BzLmhvdFJlbG9hZCgpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVhZHk6IHRydWV9KTtcbiAgICAgICAgICAgICAgICAgICAgdHJpZXMgPSAwO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH07XG4gICAgICAgICAgICB0aGlzLndzLm9uY2xvc2UgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgY29uc3QgcmVjb25uZWN0ID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICB0cmllcysrO1xuICAgICAgICAgICAgICAgICAgICBjb25uZXhpb24oKTtcbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIGlmICghaGFyZENsb3NlICYmIHRyaWVzIDwgdGhpcy5wcm9wcy5yZXRyaWVzKSB7XG4gICAgICAgICAgICAgICAgICAgIHNldFRpbWVvdXQocmVjb25uZWN0LCAxMDAwKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9O1xuICAgICAgICB9O1xuICAgICAgICBjb25uZXhpb24oKTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgdGhpcy5wYWdlQXBpKCcnLCB7bWV0aG9kOiAnUE9TVCd9KS50aGVuKHJlc3BvbnNlID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHRvUmVnZXggPSB4ID0+IG5ldyBSZWdFeHAoeCk7XG4gICAgICAgICAgICB0aGlzLnNldFN0YXRlKFxuICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgcGFnZTogcmVzcG9uc2UucGFnZSxcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0OiByZXNwb25zZS5sYXlvdXQsXG4gICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzOiBwaWNrQnkoYiA9PiAhYi5yZWdleCwgcmVzcG9uc2UuYmluZGluZ3MpLFxuICAgICAgICAgICAgICAgICAgICAvLyBSZWdleCBiaW5kaW5ncyB0cmlnZ2Vyc1xuICAgICAgICAgICAgICAgICAgICByZWJpbmRpbmdzOiBtYXAoeCA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBjb25zdCBiaW5kaW5nID0gcmVzcG9uc2UuYmluZGluZ3NbeF07XG4gICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nLnRyaWdnZXIgPSBldm9sdmUoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eTogdG9SZWdleCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0OiB0b1JlZ2V4LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZy50cmlnZ2VyXG4gICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGJpbmRpbmc7XG4gICAgICAgICAgICAgICAgICAgIH0sIGtleXMocGlja0J5KGIgPT4gYi5yZWdleCwgcmVzcG9uc2UuYmluZGluZ3MpKSksXG4gICAgICAgICAgICAgICAgICAgIHBhY2thZ2VzOiByZXNwb25zZS5wYWNrYWdlcyxcbiAgICAgICAgICAgICAgICAgICAgcmVxdWlyZW1lbnRzOiByZXNwb25zZS5yZXF1aXJlbWVudHMsXG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAoKSA9PlxuICAgICAgICAgICAgICAgICAgICBsb2FkUmVxdWlyZW1lbnRzKFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2UucmVxdWlyZW1lbnRzLFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2UucGFja2FnZXNcbiAgICAgICAgICAgICAgICAgICAgKS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChrZXlzKHJlc3BvbnNlLmJpbmRpbmdzKS5sZW5ndGggfHwgcmVzcG9uc2UucmVsb2FkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5fY29ubmVjdFdTKCk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlYWR5OiB0cnVlfSk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICApO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtsYXlvdXQsIHJlYWR5LCByZWxvYWRpbmd9ID0gdGhpcy5zdGF0ZTtcbiAgICAgICAgaWYgKCFyZWFkeSkge1xuICAgICAgICAgICAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1sb2FkaW5nXCI+TG9hZGluZy4uLjwvZGl2PjtcbiAgICAgICAgfVxuICAgICAgICBpZiAocmVsb2FkaW5nKSB7XG4gICAgICAgICAgICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJkYXp6bGVyLWxvYWRpbmdcIj5SZWxvYWRpbmcuLi48L2Rpdj47XG4gICAgICAgIH1cbiAgICAgICAgaWYgKCFpc0NvbXBvbmVudChsYXlvdXQpKSB7XG4gICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYExheW91dCBpcyBub3QgYSBjb21wb25lbnQ6ICR7bGF5b3V0fWApO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1yZW5kZXJlZFwiPlxuICAgICAgICAgICAgICAgIHtoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgICAgICBsYXlvdXQubmFtZSxcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0LnBhY2thZ2UsXG4gICAgICAgICAgICAgICAgICAgIGxheW91dC5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICAgICAgbGF5b3V0LmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuZGlzY29ubmVjdFxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICB9XG59XG5cblVwZGF0ZXIuZGVmYXVsdFByb3BzID0ge307XG5cblVwZGF0ZXIucHJvcFR5cGVzID0ge1xuICAgIGJhc2VVcmw6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBwaW5nOiBQcm9wVHlwZXMuYm9vbCxcbiAgICBwaW5nX2ludGVydmFsOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIHJldHJpZXM6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgaG90UmVsb2FkOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7Y29uY2F0LCBqb2luLCBrZXlzfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQge2NhbWVsVG9TcGluYWx9IGZyb20gJ2NvbW1vbnMnO1xuXG4vKipcbiAqIFdyYXBzIGNvbXBvbmVudHMgZm9yIGFzcGVjdHMgdXBkYXRpbmcuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFdyYXBwZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIGFzcGVjdHM6IHByb3BzLmFzcGVjdHMgfHwge30sXG4gICAgICAgICAgICByZWFkeTogZmFsc2UsXG4gICAgICAgICAgICBpbml0aWFsOiBmYWxzZSxcbiAgICAgICAgfTtcbiAgICAgICAgdGhpcy5zZXRBc3BlY3RzID0gdGhpcy5zZXRBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMuZ2V0QXNwZWN0ID0gdGhpcy5nZXRBc3BlY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzID0gdGhpcy51cGRhdGVBc3BlY3RzLmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMubWF0Y2hBc3BlY3RzID0gdGhpcy5tYXRjaEFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICB1cGRhdGVBc3BlY3RzKGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuc2V0QXNwZWN0cyhhc3BlY3RzKS50aGVuKCgpID0+XG4gICAgICAgICAgICB0aGlzLnByb3BzLnVwZGF0ZUFzcGVjdHModGhpcy5wcm9wcy5pZGVudGl0eSwgYXNwZWN0cylcbiAgICAgICAgKTtcbiAgICB9XG5cbiAgICBzZXRBc3BlY3RzKGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKHJlc29sdmUgPT4ge1xuICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZShcbiAgICAgICAgICAgICAgICB7YXNwZWN0czogey4uLnRoaXMuc3RhdGUuYXNwZWN0cywgLi4uYXNwZWN0c319LFxuICAgICAgICAgICAgICAgIHJlc29sdmVcbiAgICAgICAgICAgICk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGdldEFzcGVjdChhc3BlY3QpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuc3RhdGUuYXNwZWN0c1thc3BlY3RdO1xuICAgIH1cblxuICAgIG1hdGNoQXNwZWN0cyhwYXR0ZXJuKSB7XG4gICAgICAgIHJldHVybiBrZXlzKHRoaXMuc3RhdGUuYXNwZWN0cylcbiAgICAgICAgICAgIC5maWx0ZXIoayA9PiBwYXR0ZXJuLnRlc3QoaykpXG4gICAgICAgICAgICAubWFwKGsgPT4gW2ssIHRoaXMuc3RhdGUuYXNwZWN0c1trXV0pO1xuICAgIH1cblxuICAgIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgICAgICAvLyBPbmx5IHVwZGF0ZSB0aGUgY29tcG9uZW50IHdoZW4gbW91bnRlZC5cbiAgICAgICAgLy8gT3RoZXJ3aXNlIGdldHMgYSByYWNlIGNvbmRpdGlvbiB3aXRoIHdpbGxVbm1vdW50XG4gICAgICAgIHRoaXMucHJvcHMuY29ubmVjdChcbiAgICAgICAgICAgIHRoaXMucHJvcHMuaWRlbnRpdHksXG4gICAgICAgICAgICB0aGlzLnNldEFzcGVjdHMsXG4gICAgICAgICAgICB0aGlzLmdldEFzcGVjdCxcbiAgICAgICAgICAgIHRoaXMubWF0Y2hBc3BlY3RzXG4gICAgICAgICk7XG4gICAgICAgIGlmICghdGhpcy5zdGF0ZS5pbml0aWFsKSB7XG4gICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHModGhpcy5zdGF0ZS5hc3BlY3RzKS50aGVuKCgpID0+XG4gICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZSh7cmVhZHk6IHRydWUsIGluaXRpYWw6IHRydWV9KVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGNvbXBvbmVudFdpbGxVbm1vdW50KCkge1xuICAgICAgICB0aGlzLnByb3BzLmRpc2Nvbm5lY3QodGhpcy5wcm9wcy5pZGVudGl0eSk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7Y29tcG9uZW50LCBjb21wb25lbnRfbmFtZSwgcGFja2FnZV9uYW1lfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGNvbnN0IHthc3BlY3RzLCByZWFkeX0gPSB0aGlzLnN0YXRlO1xuICAgICAgICBpZiAoIXJlYWR5KSByZXR1cm4gbnVsbDtcblxuICAgICAgICByZXR1cm4gUmVhY3QuY2xvbmVFbGVtZW50KGNvbXBvbmVudCwge1xuICAgICAgICAgICAgLi4uYXNwZWN0cyxcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHM6IHRoaXMudXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGlkZW50aXR5OiB0aGlzLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgY2xhc3NfbmFtZTogam9pbihcbiAgICAgICAgICAgICAgICAnICcsXG4gICAgICAgICAgICAgICAgY29uY2F0KFxuICAgICAgICAgICAgICAgICAgICBbXG4gICAgICAgICAgICAgICAgICAgICAgICBgJHtwYWNrYWdlX25hbWVcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAucmVwbGFjZSgnXycsICctJylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAudG9Mb3dlckNhc2UoKX0tJHtjYW1lbFRvU3BpbmFsKGNvbXBvbmVudF9uYW1lKX1gLFxuICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICBhc3BlY3RzLmNsYXNzX25hbWUgPyBhc3BlY3RzLmNsYXNzX25hbWUuc3BsaXQoJyAnKSA6IFtdXG4gICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgKSxcbiAgICAgICAgfSk7XG4gICAgfVxufVxuXG5XcmFwcGVyLnByb3BUeXBlcyA9IHtcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuICAgIHVwZGF0ZUFzcGVjdHM6IFByb3BUeXBlcy5mdW5jLmlzUmVxdWlyZWQsXG4gICAgY29tcG9uZW50OiBQcm9wVHlwZXMubm9kZS5pc1JlcXVpcmVkLFxuICAgIGNvbm5lY3Q6IFByb3BUeXBlcy5mdW5jLmlzUmVxdWlyZWQsXG4gICAgY29tcG9uZW50X25hbWU6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBwYWNrYWdlX25hbWU6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcbiAgICBkaXNjb25uZWN0OiBQcm9wVHlwZXMuZnVuYy5pc1JlcXVpcmVkLFxufTtcbiIsImltcG9ydCB7bWFwLCBvbWl0LCB0eXBlfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFdyYXBwZXIgZnJvbSAnLi9jb21wb25lbnRzL1dyYXBwZXInO1xuXG5leHBvcnQgZnVuY3Rpb24gaXNDb21wb25lbnQoYykge1xuICAgIHJldHVybiAoXG4gICAgICAgIHR5cGUoYykgPT09ICdPYmplY3QnICYmXG4gICAgICAgIChjLmhhc093blByb3BlcnR5KCdwYWNrYWdlJykgJiZcbiAgICAgICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ2FzcGVjdHMnKSAmJlxuICAgICAgICAgICAgYy5oYXNPd25Qcm9wZXJ0eSgnbmFtZScpICYmXG4gICAgICAgICAgICBjLmhhc093blByb3BlcnR5KCdpZGVudGl0eScpKVxuICAgICk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoeWRyYXRlUHJvcHMocHJvcHMsIHVwZGF0ZUFzcGVjdHMsIGNvbm5lY3QsIGRpc2Nvbm5lY3QpIHtcbiAgICBjb25zdCByZXBsYWNlID0ge307XG4gICAgT2JqZWN0LmVudHJpZXMocHJvcHMpLmZvckVhY2goKFtrLCB2XSkgPT4ge1xuICAgICAgICBpZiAodHlwZSh2KSA9PT0gJ0FycmF5Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IHYubWFwKGMgPT4ge1xuICAgICAgICAgICAgICAgIGlmICghaXNDb21wb25lbnQoYykpIHtcbiAgICAgICAgICAgICAgICAgICAgLy8gTWl4aW5nIGNvbXBvbmVudHMgYW5kIHByaW1pdGl2ZXNcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGM7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICBjLmFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGlmICghbmV3UHJvcHMua2V5KSB7XG4gICAgICAgICAgICAgICAgICAgIG5ld1Byb3BzLmtleSA9IGMuaWRlbnRpdHk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgICAgICBjLm5hbWUsXG4gICAgICAgICAgICAgICAgICAgIGMucGFja2FnZSxcbiAgICAgICAgICAgICAgICAgICAgYy5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgbmV3UHJvcHMsXG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3RcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH0gZWxzZSBpZiAoaXNDb21wb25lbnQodikpIHtcbiAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgIHYuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIHJlcGxhY2Vba10gPSBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgICAgIHYubmFtZSxcbiAgICAgICAgICAgICAgICB2LnBhY2thZ2UsXG4gICAgICAgICAgICAgICAgdi5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICBuZXdQcm9wcyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSBlbHNlIGlmICh0eXBlKHYpID09PSAnT2JqZWN0Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IGh5ZHJhdGVQcm9wcyh2LCB1cGRhdGVBc3BlY3RzLCBjb25uZWN0LCBkaXNjb25uZWN0KTtcbiAgICAgICAgfVxuICAgIH0pO1xuICAgIHJldHVybiB7Li4ucHJvcHMsIC4uLnJlcGxhY2V9O1xufVxuXG5leHBvcnQgZnVuY3Rpb24gaHlkcmF0ZUNvbXBvbmVudChcbiAgICBuYW1lLFxuICAgIHBhY2thZ2VfbmFtZSxcbiAgICBpZGVudGl0eSxcbiAgICBwcm9wcyxcbiAgICB1cGRhdGVBc3BlY3RzLFxuICAgIGNvbm5lY3QsXG4gICAgZGlzY29ubmVjdFxuKSB7XG4gICAgY29uc3QgcGFjayA9IHdpbmRvd1twYWNrYWdlX25hbWVdO1xuICAgIGNvbnN0IGVsZW1lbnQgPSBSZWFjdC5jcmVhdGVFbGVtZW50KHBhY2tbbmFtZV0sIHByb3BzKTtcbiAgICByZXR1cm4gKFxuICAgICAgICA8V3JhcHBlclxuICAgICAgICAgICAgaWRlbnRpdHk9e2lkZW50aXR5fVxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cz17dXBkYXRlQXNwZWN0c31cbiAgICAgICAgICAgIGNvbXBvbmVudD17ZWxlbWVudH1cbiAgICAgICAgICAgIGNvbm5lY3Q9e2Nvbm5lY3R9XG4gICAgICAgICAgICBwYWNrYWdlX25hbWU9e3BhY2thZ2VfbmFtZX1cbiAgICAgICAgICAgIGNvbXBvbmVudF9uYW1lPXtuYW1lfVxuICAgICAgICAgICAgYXNwZWN0cz17cHJvcHN9XG4gICAgICAgICAgICBkaXNjb25uZWN0PXtkaXNjb25uZWN0fVxuICAgICAgICAgICAga2V5PXtgd3JhcHBlci0ke2lkZW50aXR5fWB9XG4gICAgICAgIC8+XG4gICAgKTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHByZXBhcmVQcm9wKHByb3ApIHtcbiAgICBpZiAoUmVhY3QuaXNWYWxpZEVsZW1lbnQocHJvcCkpIHtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICAgIGlkZW50aXR5OiBwcm9wLnByb3BzLmlkZW50aXR5LFxuICAgICAgICAgICAgYXNwZWN0czogbWFwKFxuICAgICAgICAgICAgICAgIHByZXBhcmVQcm9wLFxuICAgICAgICAgICAgICAgIG9taXQoXG4gICAgICAgICAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgICAgICAgICAgICdpZGVudGl0eScsXG4gICAgICAgICAgICAgICAgICAgICAgICAndXBkYXRlQXNwZWN0cycsXG4gICAgICAgICAgICAgICAgICAgICAgICAnX25hbWUnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ19wYWNrYWdlJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdhc3BlY3RzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdrZXknLFxuICAgICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgICBwcm9wLnByb3BzLmFzcGVjdHNcbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICApLFxuICAgICAgICAgICAgbmFtZTogcHJvcC5wcm9wcy5jb21wb25lbnRfbmFtZSxcbiAgICAgICAgICAgIHBhY2thZ2U6IHByb3AucHJvcHMucGFja2FnZV9uYW1lLFxuICAgICAgICB9O1xuICAgIH1cbiAgICBpZiAodHlwZShwcm9wKSA9PT0gJ0FycmF5Jykge1xuICAgICAgICByZXR1cm4gcHJvcC5tYXAocHJlcGFyZVByb3ApO1xuICAgIH1cbiAgICBpZiAodHlwZShwcm9wKSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgcmV0dXJuIG1hcChwcmVwYXJlUHJvcCwgcHJvcCk7XG4gICAgfVxuICAgIHJldHVybiBwcm9wO1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBSZWFjdERPTSBmcm9tICdyZWFjdC1kb20nO1xuaW1wb3J0IFJlbmRlcmVyIGZyb20gJy4vY29tcG9uZW50cy9SZW5kZXJlcic7XG5cbmZ1bmN0aW9uIHJlbmRlcih7YmFzZVVybCwgcGluZywgcGluZ19pbnRlcnZhbCwgcmV0cmllc30sIGVsZW1lbnQpIHtcbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIDxSZW5kZXJlclxuICAgICAgICAgICAgYmFzZVVybD17YmFzZVVybH1cbiAgICAgICAgICAgIHBpbmc9e3Bpbmd9XG4gICAgICAgICAgICBwaW5nX2ludGVydmFsPXtwaW5nX2ludGVydmFsfVxuICAgICAgICAgICAgcmV0cmllcz17cmV0cmllc31cbiAgICAgICAgLz4sXG4gICAgICAgIGVsZW1lbnRcbiAgICApO1xufVxuXG5leHBvcnQge1JlbmRlcmVyLCByZW5kZXJ9O1xuIiwiLyogZXNsaW50LWRpc2FibGUgbm8tbWFnaWMtbnVtYmVycyAqL1xuXG5jb25zdCBqc29uUGF0dGVybiA9IC9qc29uL2k7XG5cbi8qKlxuICogQHR5cGVkZWYge09iamVjdH0gWGhyT3B0aW9uc1xuICogQHByb3BlcnR5IHtzdHJpbmd9IFttZXRob2Q9J0dFVCddXG4gKiBAcHJvcGVydHkge09iamVjdH0gW2hlYWRlcnM9e31dXG4gKiBAcHJvcGVydHkge3N0cmluZ3xCbG9ifEFycmF5QnVmZmVyfG9iamVjdHxBcnJheX0gW3BheWxvYWQ9JyddXG4gKi9cblxuLyoqXG4gKiBAdHlwZSB7WGhyT3B0aW9uc31cbiAqL1xuY29uc3QgZGVmYXVsdFhock9wdGlvbnMgPSB7XG4gICAgbWV0aG9kOiAnR0VUJyxcbiAgICBoZWFkZXJzOiB7fSxcbiAgICBwYXlsb2FkOiAnJyxcbiAgICBqc29uOiB0cnVlLFxufTtcblxuZXhwb3J0IGNvbnN0IEpTT05IRUFERVJTID0ge1xuICAgICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbicsXG59O1xuXG4vKipcbiAqIFhociBwcm9taXNlIHdyYXAuXG4gKlxuICogRmV0Y2ggY2FuJ3QgZG8gcHV0IHJlcXVlc3QsIHNvIHhociBzdGlsbCB1c2VmdWwuXG4gKlxuICogQXV0byBwYXJzZSBqc29uIHJlc3BvbnNlcy5cbiAqIENhbmNlbGxhdGlvbjogeGhyLmFib3J0XG4gKiBAcGFyYW0ge3N0cmluZ30gdXJsXG4gKiBAcGFyYW0ge1hock9wdGlvbnN9IFtvcHRpb25zXVxuICogQHJldHVybiB7UHJvbWlzZX1cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHhoclJlcXVlc3QodXJsLCBvcHRpb25zID0gZGVmYXVsdFhock9wdGlvbnMpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7bWV0aG9kLCBoZWFkZXJzLCBwYXlsb2FkLCBqc29ufSA9IHtcbiAgICAgICAgICAgIC4uLmRlZmF1bHRYaHJPcHRpb25zLFxuICAgICAgICAgICAgLi4ub3B0aW9ucyxcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgeGhyID0gbmV3IFhNTEh0dHBSZXF1ZXN0KCk7XG4gICAgICAgIHhoci5vcGVuKG1ldGhvZCwgdXJsKTtcbiAgICAgICAgY29uc3QgaGVhZCA9IGpzb24gPyB7Li4uSlNPTkhFQURFUlMsIC4uLmhlYWRlcnN9IDogaGVhZGVycztcbiAgICAgICAgT2JqZWN0LmtleXMoaGVhZCkuZm9yRWFjaChrID0+IHhoci5zZXRSZXF1ZXN0SGVhZGVyKGssIGhlYWRba10pKTtcbiAgICAgICAgeGhyLm9ucmVhZHlzdGF0ZWNoYW5nZSA9ICgpID0+IHtcbiAgICAgICAgICAgIGlmICh4aHIucmVhZHlTdGF0ZSA9PT0gWE1MSHR0cFJlcXVlc3QuRE9ORSkge1xuICAgICAgICAgICAgICAgIGlmICh4aHIuc3RhdHVzIDwgNDAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCByZXNwb25zZVZhbHVlID0geGhyLnJlc3BvbnNlO1xuICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICBqc29uUGF0dGVybi50ZXN0KHhoci5nZXRSZXNwb25zZUhlYWRlcignQ29udGVudC1UeXBlJykpXG4gICAgICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2VWYWx1ZSA9IEpTT04ucGFyc2UoeGhyLnJlc3BvbnNlVGV4dCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZShyZXNwb25zZVZhbHVlKTtcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICByZWplY3Qoe1xuICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3I6ICdSZXF1ZXN0RXJyb3InLFxuICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZTogYFhIUiAke3VybH0gRkFJTEVEIC0gU1RBVFVTOiAke1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHhoci5zdGF0dXNcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gTUVTU0FHRTogJHt4aHIuc3RhdHVzVGV4dH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgc3RhdHVzOiB4aHIuc3RhdHVzLFxuICAgICAgICAgICAgICAgICAgICAgICAgeGhyLFxuICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIHhoci5vbmVycm9yID0gZXJyID0+IHJlamVjdChlcnIpO1xuICAgICAgICB4aHIuc2VuZChqc29uID8gSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkgOiBwYXlsb2FkKTtcbiAgICB9KTtcbn1cblxuLyoqXG4gKiBBdXRvIGdldCBoZWFkZXJzIGFuZCByZWZyZXNoL3JldHJ5LlxuICpcbiAqIEBwYXJhbSB7ZnVuY3Rpb259IGdldEhlYWRlcnNcbiAqIEBwYXJhbSB7ZnVuY3Rpb259IHJlZnJlc2hcbiAqIEBwYXJhbSB7c3RyaW5nfSBiYXNlVXJsXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBhcGlSZXF1ZXN0KGJhc2VVcmwgPSAnJykge1xuICAgIHJldHVybiBmdW5jdGlvbigpIHtcbiAgICAgICAgY29uc3QgdXJsID0gYmFzZVVybCArIGFyZ3VtZW50c1swXTtcbiAgICAgICAgY29uc3Qgb3B0aW9ucyA9IGFyZ3VtZW50c1sxXSB8fCB7fTtcbiAgICAgICAgb3B0aW9ucy5oZWFkZXJzID0gey4uLm9wdGlvbnMuaGVhZGVyc307XG4gICAgICAgIHJldHVybiBuZXcgUHJvbWlzZShyZXNvbHZlID0+IHtcbiAgICAgICAgICAgIHhoclJlcXVlc3QodXJsLCBvcHRpb25zKS50aGVuKHJlc29sdmUpO1xuICAgICAgICB9KTtcbiAgICB9O1xufVxuIiwiaW1wb3J0IHtsb2FkQ3NzLCBsb2FkU2NyaXB0fSBmcm9tICdjb21tb25zJztcblxuZXhwb3J0IGZ1bmN0aW9uIGxvYWRSZXF1aXJlbWVudChyZXF1aXJlbWVudCkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHt1cmwsIGtpbmQsIG1ldGF9ID0gcmVxdWlyZW1lbnQ7XG4gICAgICAgIGxldCBtZXRob2Q7XG4gICAgICAgIGlmIChraW5kID09PSAnanMnKSB7XG4gICAgICAgICAgICBtZXRob2QgPSBsb2FkU2NyaXB0O1xuICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdjc3MnKSB7XG4gICAgICAgICAgICBtZXRob2QgPSBsb2FkQ3NzO1xuICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdtYXAnKSB7XG4gICAgICAgICAgICByZXR1cm4gcmVzb2x2ZSgpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIHJlamVjdCh7ZXJyb3I6IGBJbnZhbGlkIHJlcXVpcmVtZW50IGtpbmQ6ICR7a2luZH1gfSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIG1ldGhvZCh1cmwsIG1ldGEpXG4gICAgICAgICAgICAudGhlbihyZXNvbHZlKVxuICAgICAgICAgICAgLmNhdGNoKHJlamVjdCk7XG4gICAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBsb2FkUmVxdWlyZW1lbnRzKHJlcXVpcmVtZW50cywgcGFja2FnZXMpIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBsZXQgbG9hZGluZ3MgPSBbXTtcbiAgICAgICAgLy8gTG9hZCBwYWNrYWdlcyBmaXJzdC5cbiAgICAgICAgT2JqZWN0LmtleXMocGFja2FnZXMpLmZvckVhY2gocGFja19uYW1lID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHBhY2sgPSBwYWNrYWdlc1twYWNrX25hbWVdO1xuICAgICAgICAgICAgbG9hZGluZ3MgPSBsb2FkaW5ncy5jb25jYXQocGFjay5yZXF1aXJlbWVudHMubWFwKGxvYWRSZXF1aXJlbWVudCkpO1xuICAgICAgICB9KTtcbiAgICAgICAgLy8gVGhlbiBsb2FkIHJlcXVpcmVtZW50cyBzbyB0aGV5IGNhbiB1c2UgcGFja2FnZXNcbiAgICAgICAgLy8gYW5kIG92ZXJyaWRlIGNzcy5cbiAgICAgICAgUHJvbWlzZS5hbGwobG9hZGluZ3MpXG4gICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgbGV0IGkgPSAwO1xuICAgICAgICAgICAgICAgIC8vIExvYWQgaW4gb3JkZXIuXG4gICAgICAgICAgICAgICAgY29uc3QgaGFuZGxlciA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGkgPCByZXF1aXJlbWVudHMubGVuZ3RoKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBsb2FkUmVxdWlyZW1lbnQocmVxdWlyZW1lbnRzW2ldKS50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpKys7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaGFuZGxlcigpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICAgIGhhbmRsZXIoKTtcbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAuY2F0Y2gocmVqZWN0KTtcbiAgICB9KTtcbn1cbiIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9kb21fXzsiXSwic291cmNlUm9vdCI6IiJ9
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_extra"] = factory(require("react"));
	else
		root["dazzler_extra"] = factory(root["React"]);
})(window, function(__WEBPACK_EXTERNAL_MODULE_react__) {
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
/******/ 		"extra": 0
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
/******/ 	deferredModules.push([4,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/extra/scss/index.scss":
/*!************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/extra/scss/index.scss ***!
  \************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./src/extra/js/components/Drawer.jsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Drawer.jsx ***!
  \********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Drawer; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var Caret = function Caret(_ref) {
  var side = _ref.side,
      opened = _ref.opened;

  switch (side) {
    case 'top':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B2") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25BC");

    case 'right':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B8") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25C2");

    case 'left':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25C2") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B8");

    case 'bottom':
      return opened ? react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25BC") : react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", null, "\u25B2");
  }
};
/**
 * Draw content from the sides of the screen.
 */


var Drawer =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Drawer, _React$Component);

  function Drawer() {
    _classCallCheck(this, Drawer);

    return _possibleConstructorReturn(this, _getPrototypeOf(Drawer).apply(this, arguments));
  }

  _createClass(Drawer, [{
    key: "render",
    value: function render() {
      var _this = this;

      var _this$props = this.props,
          class_name = _this$props.class_name,
          identity = _this$props.identity,
          style = _this$props.style,
          children = _this$props.children,
          opened = _this$props.opened,
          side = _this$props.side;
      var css = [side];

      if (side === 'top' || side === 'bottom') {
        css.push('horizontal');
      } else {
        css.push('vertical');
      }

      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(css, [class_name])),
        id: identity,
        style: style
      }, opened && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(css, ['drawer-content']))
      }, children), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_2__["concat"])(css, ['drawer-control'])),
        onClick: function onClick() {
          return _this.props.updateAspects({
            opened: !opened
          });
        }
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Caret, {
        opened: opened,
        side: side
      })));
    }
  }]);

  return Drawer;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Drawer.defaultProps = {
  side: 'top'
};
Drawer.propTypes = {
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,
  opened: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Side which open.
   */
  side: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['top', 'left', 'right', 'bottom']),

  /**
   *  Unique id for this component
   */
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Update aspects on the backend.
   */
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Notice.jsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Notice.jsx ***!
  \********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Notice; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var commons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! commons */ "./src/commons/js/index.js");
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * Browser notifications with permissions handling.
 */

var Notice =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Notice, _React$Component);

  function Notice(props) {
    var _this;

    _classCallCheck(this, Notice);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Notice).call(this, props));
    _this.state = {
      lastMessage: props.body,
      notification: null
    };
    _this.onPermission = _this.onPermission.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Notice, [{
    key: "componentDidMount",
    value: function componentDidMount() {
      var updateAspects = this.props.updateAspects;

      if (!('Notification' in window) && updateAspects) {
        updateAspects({
          permission: 'unsupported'
        });
      } else if (Notification.permission === 'default') {
        Notification.requestPermission().then(this.onPermission);
      } else {
        this.onPermission(window.Notification.permission);
      }
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate(prevProps) {
      if (!prevProps.displayed && this.props.displayed) {
        this.sendNotification(this.props.permission);
      }
    }
  }, {
    key: "sendNotification",
    value: function sendNotification(permission) {
      var _this2 = this;

      var _this$props = this.props,
          updateAspects = _this$props.updateAspects,
          body = _this$props.body,
          title = _this$props.title,
          icon = _this$props.icon,
          require_interaction = _this$props.require_interaction,
          lang = _this$props.lang,
          badge = _this$props.badge,
          tag = _this$props.tag,
          image = _this$props.image,
          vibrate = _this$props.vibrate;

      if (permission === 'granted') {
        var options = {
          requireInteraction: require_interaction,
          body: body,
          icon: icon,
          lang: lang,
          badge: badge,
          tag: tag,
          image: image,
          vibrate: vibrate
        };
        var notification = new Notification(title, options);

        notification.onclick = function () {
          if (updateAspects) {
            updateAspects(Object(ramda__WEBPACK_IMPORTED_MODULE_3__["merge"])({
              displayed: false
            }, Object(commons__WEBPACK_IMPORTED_MODULE_2__["timestampProp"])('clicks', _this2.props.clicks + 1)));
          }
        };

        notification.onclose = function () {
          if (updateAspects) {
            updateAspects(Object(ramda__WEBPACK_IMPORTED_MODULE_3__["merge"])({
              displayed: false
            }, Object(commons__WEBPACK_IMPORTED_MODULE_2__["timestampProp"])('closes', _this2.props.closes + 1)));
          }
        };
      }
    }
  }, {
    key: "onPermission",
    value: function onPermission(permission) {
      var _this$props2 = this.props,
          displayed = _this$props2.displayed,
          updateAspects = _this$props2.updateAspects;

      if (updateAspects) {
        updateAspects({
          permission: permission
        });
      }

      if (displayed) {
        this.sendNotification(permission);
      }
    }
  }, {
    key: "render",
    value: function render() {
      return null;
    }
  }]);

  return Notice;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Notice.defaultProps = {
  require_interaction: false,
  clicks: 0,
  clicks_timestamp: -1,
  closes: 0,
  closes_timestamp: -1
}; // Props docs from https://developer.mozilla.org/en-US/docs/Web/API/Notification/Notification

Notice.propTypes = {
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Permission granted by the user (READONLY)
   */
  permission: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['denied', 'granted', 'default', 'unsupported']),
  title: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,

  /**
   * The notification's language, as specified using a DOMString representing a BCP 47 language tag.
   */
  lang: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A DOMString representing the body text of the notification, which will be displayed below the title.
   */
  body: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A USVString containing the URL of the image used to represent the notification when there is not enough space to display the notification itself.
   */
  badge: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A DOMString representing an identifying tag for the notification.
   */
  tag: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A USVString containing the URL of an icon to be displayed in the notification.
   */
  icon: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   *  a USVString containing the URL of an image to be displayed in the notification.
   */
  image: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * A vibration pattern for the device's vibration hardware to emit when the notification fires.
   */
  vibrate: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOfType([prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number, prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number)]),

  /**
   * Indicates that a notification should remain active until the user clicks or dismisses it, rather than closing automatically. The default value is false.
   */
  require_interaction: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,

  /**
   * Set to true to display the notification.
   */
  displayed: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  clicks: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  clicks_timestamp: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * Number of times the notification was closed.
   */
  closes: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  closes_timestamp: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  updateAspect: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Pager.jsx":
/*!*******************************************!*\
  !*** ./src/extra/js/components/Pager.jsx ***!
  \*******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Pager; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





var startOffset = function startOffset(page, itemPerPage) {
  return (page - 1) * (page > 1 ? itemPerPage : 0);
};

var endOffset = function endOffset(start, itemPerPage, page, total, leftOver) {
  return page !== total ? start + itemPerPage : leftOver !== 0 ? start + leftOver : start + itemPerPage;
};

var showList = function showList(page, total, n) {
  if (total > n) {
    var middle = n / 2;
    var first = page >= total - middle ? total - n + 1 : page > middle ? page - middle : 1;
    var last = page < total - middle ? first + n : total + 1;
    return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["range"])(first, last);
  }

  return Object(ramda__WEBPACK_IMPORTED_MODULE_2__["range"])(1, total + 1);
};

var Page = function Page(_ref) {
  var style = _ref.style,
      class_name = _ref.class_name,
      on_change = _ref.on_change,
      text = _ref.text,
      page = _ref.page;
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span", {
    style: style,
    className: class_name,
    onClick: function onClick() {
      return on_change(page);
    }
  }, text || page);
};
/**
 * Paging for dazzler apps.
 */


var Pager =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Pager, _React$Component);

  function Pager(props) {
    var _this;

    _classCallCheck(this, Pager);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(Pager).call(this, props));
    _this.state = {
      current_page: null,
      start_offset: null,
      end_offset: null,
      pages: [],
      total_pages: Math.ceil(props.total_items / props.items_per_page)
    };
    _this.onChangePage = _this.onChangePage.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(Pager, [{
    key: "componentWillMount",
    value: function componentWillMount() {
      this.onChangePage(this.props.current_page);
    }
  }, {
    key: "onChangePage",
    value: function onChangePage(page) {
      var _this$props = this.props,
          items_per_page = _this$props.items_per_page,
          total_items = _this$props.total_items,
          updateAspects = _this$props.updateAspects,
          pages_displayed = _this$props.pages_displayed;
      var total_pages = this.state.total_pages;
      var start_offset = startOffset(page, items_per_page);
      var leftOver = total_items % items_per_page;
      var end_offset = endOffset(start_offset, items_per_page, page, total_pages, leftOver);
      var payload = {
        current_page: page,
        start_offset: start_offset,
        end_offset: end_offset,
        pages: showList(page, total_pages, pages_displayed)
      };
      this.setState(payload);

      if (updateAspects) {
        if (this.state.total_pages !== this.props.total_pages) {
          payload.total_pages = this.state.total_pages;
        }

        updateAspects(payload);
      }
    }
  }, {
    key: "componentWillReceiveProps",
    value: function componentWillReceiveProps(props) {
      if (props.current_page !== this.state.current_page) {
        this.onChangePage(props.current_page);
      }
    }
  }, {
    key: "render",
    value: function render() {
      var _this2 = this;

      var _this$state = this.state,
          current_page = _this$state.current_page,
          pages = _this$state.pages,
          total_pages = _this$state.total_pages;
      var _this$props2 = this.props,
          class_name = _this$props2.class_name,
          identity = _this$props2.identity,
          page_style = _this$props2.page_style,
          page_class_name = _this$props2.page_class_name;
      var pageCss = ['page'];

      if (page_class_name) {
        pageCss.push(page_class_name);
      }

      pageCss = Object(ramda__WEBPACK_IMPORTED_MODULE_2__["join"])(' ', pageCss);
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: class_name,
        id: identity
      }, current_page > 1 && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: 1,
        text: 'first',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }), current_page > 1 && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: current_page - 1,
        text: 'previous',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }), pages.map(function (e) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
          page: e,
          key: "page-".concat(e),
          style: page_style,
          class_name: pageCss,
          on_change: _this2.onChangePage
        });
      }), current_page < total_pages && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: current_page + 1,
        text: 'next',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }), current_page < total_pages && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Page, {
        page: total_pages,
        text: 'last',
        style: page_style,
        class_name: pageCss,
        on_change: this.onChangePage
      }));
    }
  }]);

  return Pager;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Pager.defaultProps = {
  current_page: 1,
  items_per_page: 10,
  pages_displayed: 10
};
Pager.propTypes = {
  /**
   * The total items in the set.
   */
  total_items: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number.isRequired,

  /**
   * The number of items a page contains.
   */
  items_per_page: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Style for the page numbers.
   */
  page_style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,

  /**
   * CSS class for the page numbers.
   */
  page_class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * The number of pages displayed by the pager.
   */
  pages_displayed: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * Read only, the currently displayed pages numbers.
   */
  pages: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,

  /**
   * The current selected page.
   */
  current_page: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * Set by total_items / items_per_page
   */
  total_pages: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * The starting index of the current page
   * Can be used to slice data eg: data[start_offset: end_offset]
   */
  start_offset: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,

  /**
   * The end index of the current page.
   */
  end_offset: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/PopUp.jsx":
/*!*******************************************!*\
  !*** ./src/extra/js/components/PopUp.jsx ***!
  \*******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return PopUp; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }




function getMouseX(e, popup) {
  return e.clientX - e.target.getBoundingClientRect().left - popup.getBoundingClientRect().width / 2;
}
/**
 * Wraps a component/text to render a popup when hovering
 * over the children or clicking on it.
 */


var PopUp =
/*#__PURE__*/
function (_React$Component) {
  _inherits(PopUp, _React$Component);

  function PopUp(props) {
    var _this;

    _classCallCheck(this, PopUp);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(PopUp).call(this, props));
    _this.state = {
      pos: null
    };
    return _this;
  }

  _createClass(PopUp, [{
    key: "render",
    value: function render() {
      var _this2 = this;

      var _this$props = this.props,
          class_name = _this$props.class_name,
          style = _this$props.style,
          identity = _this$props.identity,
          children = _this$props.children,
          content = _this$props.content,
          mode = _this$props.mode,
          updateAspects = _this$props.updateAspects,
          active = _this$props.active,
          content_style = _this$props.content_style,
          children_style = _this$props.children_style;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: class_name,
        style: style,
        id: identity
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: 'popup-content' + (active ? ' visible' : ''),
        style: _objectSpread({}, content_style || {}, {
          left: this.state.pos || 0
        }),
        ref: function ref(r) {
          return _this2.popupRef = r;
        }
      }, content), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "popup-children",
        onMouseEnter: function onMouseEnter(e) {
          if (mode === 'hover') {
            _this2.setState({
              pos: getMouseX(e, _this2.popupRef)
            }, function () {
              return updateAspects({
                active: true
              });
            });
          }
        },
        onMouseLeave: function onMouseLeave() {
          return mode === 'hover' && updateAspects({
            active: false
          });
        },
        onClick: function onClick(e) {
          if (mode === 'click') {
            _this2.setState({
              pos: getMouseX(e, _this2.popupRef)
            }, function () {
              return updateAspects({
                active: !active
              });
            });
          }
        },
        style: children_style
      }, children));
    }
  }]);

  return PopUp;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


PopUp.defaultProps = {
  mode: 'hover',
  active: false
};
PopUp.propTypes = {
  /**
   * Component/text to wrap with a popup on hover/click.
   */
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,

  /**
   * Content of the popup info.
   */
  content: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,

  /**
   * Is the popup currently active.
   */
  active: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,

  /**
   * Show popup on hover or click.
   */
  mode: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['hover', 'click']),

  /**
   * CSS for the wrapper.
   */
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Style of the wrapper.
   */
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,

  /**
   * Style for the popup.
   */
  content_style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,

  /**
   * Style for the wrapped children.
   */
  children_style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Spinner.jsx":
/*!*********************************************!*\
  !*** ./src/extra/js/components/Spinner.jsx ***!
  \*********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Spinner; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }



/**
 * Simple html/css spinner.
 */

var Spinner =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Spinner, _React$Component);

  function Spinner() {
    _classCallCheck(this, Spinner);

    return _possibleConstructorReturn(this, _getPrototypeOf(Spinner).apply(this, arguments));
  }

  _createClass(Spinner, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          class_name = _this$props.class_name,
          style = _this$props.style,
          identity = _this$props.identity;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: identity,
        className: class_name,
        style: style
      });
    }
  }]);

  return Spinner;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Spinner.defaultProps = {};
Spinner.propTypes = {
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,

  /**
   *  Unique id for this component
   */
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Update aspects on the backend.
   */
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/extra/js/components/Sticky.jsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Sticky.jsx ***!
  \********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Sticky; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ramda__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }




/**
 * A shorthand component for a sticky div.
 */

var Sticky =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Sticky, _React$Component);

  function Sticky() {
    _classCallCheck(this, Sticky);

    return _possibleConstructorReturn(this, _getPrototypeOf(Sticky).apply(this, arguments));
  }

  _createClass(Sticky, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          class_name = _this$props.class_name,
          identity = _this$props.identity,
          style = _this$props.style,
          children = _this$props.children,
          top = _this$props.top,
          left = _this$props.left,
          right = _this$props.right,
          bottom = _this$props.bottom;
      var styles = Object(ramda__WEBPACK_IMPORTED_MODULE_2__["mergeAll"])([style, {
        top: top,
        left: left,
        right: right,
        bottom: bottom
      }]);
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: class_name,
        id: identity,
        style: styles
      }, children);
    }
  }]);

  return Sticky;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Sticky.defaultProps = {}; // TODO Add Sticky props descriptions

Sticky.propTypes = {
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,
  top: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  left: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  right: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  bottom: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string
};

/***/ }),

/***/ "./src/extra/js/index.js":
/*!*******************************!*\
  !*** ./src/extra/js/index.js ***!
  \*******************************/
/*! exports provided: Notice, Pager, Spinner, Sticky, Drawer, PopUp */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _scss_index_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../scss/index.scss */ "./src/extra/scss/index.scss");
/* harmony import */ var _scss_index_scss__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_scss_index_scss__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_Notice__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/Notice */ "./src/extra/js/components/Notice.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Notice", function() { return _components_Notice__WEBPACK_IMPORTED_MODULE_1__["default"]; });

/* harmony import */ var _components_Pager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Pager */ "./src/extra/js/components/Pager.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Pager", function() { return _components_Pager__WEBPACK_IMPORTED_MODULE_2__["default"]; });

/* harmony import */ var _components_Spinner__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/Spinner */ "./src/extra/js/components/Spinner.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Spinner", function() { return _components_Spinner__WEBPACK_IMPORTED_MODULE_3__["default"]; });

/* harmony import */ var _components_Sticky__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/Sticky */ "./src/extra/js/components/Sticky.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Sticky", function() { return _components_Sticky__WEBPACK_IMPORTED_MODULE_4__["default"]; });

/* harmony import */ var _components_Drawer__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/Drawer */ "./src/extra/js/components/Drawer.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Drawer", function() { return _components_Drawer__WEBPACK_IMPORTED_MODULE_5__["default"]; });

/* harmony import */ var _components_PopUp__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/PopUp */ "./src/extra/js/components/PopUp.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "PopUp", function() { return _components_PopUp__WEBPACK_IMPORTED_MODULE_6__["default"]; });










/***/ }),

/***/ "./src/extra/scss/index.scss":
/*!***********************************!*\
  !*** ./src/extra/scss/index.scss ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../../../node_modules/mini-css-extract-plugin/dist/loader.js!../../../node_modules/css-loader/dist/cjs.js!../../../node_modules/sass-loader/lib/loader.js!./index.scss */ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/extra/scss/index.scss");

if(typeof content === 'string') content = [[module.i, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! ../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ 4:
/*!*************************************!*\
  !*** multi ./src/extra/js/index.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/extra/js/index.js */"./src/extra/js/index.js");


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

/******/ });
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8uL3NyYy9leHRyYS9zY3NzL2luZGV4LnNjc3M/Li9ub2RlX21vZHVsZXMvbWluaS1jc3MtZXh0cmFjdC1wbHVnaW4vZGlzdC9sb2FkZXIuanMhLi9ub2RlX21vZHVsZXMvY3NzLWxvYWRlci9kaXN0L2Nqcy5qcyEuL25vZGVfbW9kdWxlcy9zYXNzLWxvYWRlci9saWIvbG9hZGVyLmpzIiwid2VicGFjazovLy8uL3NyYy9leHRyYS9qcy9jb21wb25lbnRzL0RyYXdlci5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9leHRyYS9qcy9jb21wb25lbnRzL05vdGljZS5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9leHRyYS9qcy9jb21wb25lbnRzL1BhZ2VyLmpzeD8iLCJ3ZWJwYWNrOi8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvUG9wVXAuanN4PyIsIndlYnBhY2s6Ly8vLi9zcmMvZXh0cmEvanMvY29tcG9uZW50cy9TcGlubmVyLmpzeD8iLCJ3ZWJwYWNrOi8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvU3RpY2t5LmpzeD8iLCJ3ZWJwYWNrOi8vLy4vc3JjL2V4dHJhL2pzL2luZGV4LmpzPyIsIndlYnBhY2s6Ly8vLi9zcmMvZXh0cmEvc2Nzcy9pbmRleC5zY3NzPyIsIndlYnBhY2s6Ly8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iXSwibmFtZXMiOlsiQ2FyZXQiLCJzaWRlIiwib3BlbmVkIiwiRHJhd2VyIiwicHJvcHMiLCJjbGFzc19uYW1lIiwiaWRlbnRpdHkiLCJzdHlsZSIsImNoaWxkcmVuIiwiY3NzIiwicHVzaCIsImpvaW4iLCJjb25jYXQiLCJ1cGRhdGVBc3BlY3RzIiwiUmVhY3QiLCJDb21wb25lbnQiLCJkZWZhdWx0UHJvcHMiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJub2RlIiwiYm9vbCIsIm9iamVjdCIsInN0cmluZyIsIm9uZU9mIiwiZnVuYyIsIk5vdGljZSIsInN0YXRlIiwibGFzdE1lc3NhZ2UiLCJib2R5Iiwibm90aWZpY2F0aW9uIiwib25QZXJtaXNzaW9uIiwiYmluZCIsIndpbmRvdyIsInBlcm1pc3Npb24iLCJOb3RpZmljYXRpb24iLCJyZXF1ZXN0UGVybWlzc2lvbiIsInRoZW4iLCJwcmV2UHJvcHMiLCJkaXNwbGF5ZWQiLCJzZW5kTm90aWZpY2F0aW9uIiwidGl0bGUiLCJpY29uIiwicmVxdWlyZV9pbnRlcmFjdGlvbiIsImxhbmciLCJiYWRnZSIsInRhZyIsImltYWdlIiwidmlicmF0ZSIsIm9wdGlvbnMiLCJyZXF1aXJlSW50ZXJhY3Rpb24iLCJvbmNsaWNrIiwibWVyZ2UiLCJ0aW1lc3RhbXBQcm9wIiwiY2xpY2tzIiwib25jbG9zZSIsImNsb3NlcyIsImNsaWNrc190aW1lc3RhbXAiLCJjbG9zZXNfdGltZXN0YW1wIiwiaXNSZXF1aXJlZCIsIm9uZU9mVHlwZSIsIm51bWJlciIsImFycmF5T2YiLCJ1cGRhdGVBc3BlY3QiLCJzdGFydE9mZnNldCIsInBhZ2UiLCJpdGVtUGVyUGFnZSIsImVuZE9mZnNldCIsInN0YXJ0IiwidG90YWwiLCJsZWZ0T3ZlciIsInNob3dMaXN0IiwibiIsIm1pZGRsZSIsImZpcnN0IiwibGFzdCIsInJhbmdlIiwiUGFnZSIsIm9uX2NoYW5nZSIsInRleHQiLCJQYWdlciIsImN1cnJlbnRfcGFnZSIsInN0YXJ0X29mZnNldCIsImVuZF9vZmZzZXQiLCJwYWdlcyIsInRvdGFsX3BhZ2VzIiwiTWF0aCIsImNlaWwiLCJ0b3RhbF9pdGVtcyIsIml0ZW1zX3Blcl9wYWdlIiwib25DaGFuZ2VQYWdlIiwicGFnZXNfZGlzcGxheWVkIiwicGF5bG9hZCIsInNldFN0YXRlIiwicGFnZV9zdHlsZSIsInBhZ2VfY2xhc3NfbmFtZSIsInBhZ2VDc3MiLCJtYXAiLCJlIiwiYXJyYXkiLCJnZXRNb3VzZVgiLCJwb3B1cCIsImNsaWVudFgiLCJ0YXJnZXQiLCJnZXRCb3VuZGluZ0NsaWVudFJlY3QiLCJsZWZ0Iiwid2lkdGgiLCJQb3BVcCIsInBvcyIsImNvbnRlbnQiLCJtb2RlIiwiYWN0aXZlIiwiY29udGVudF9zdHlsZSIsImNoaWxkcmVuX3N0eWxlIiwiciIsInBvcHVwUmVmIiwiU3Bpbm5lciIsIlN0aWNreSIsInRvcCIsInJpZ2h0IiwiYm90dG9tIiwic3R5bGVzIiwibWVyZ2VBbGwiXSwibWFwcGluZ3MiOiJBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLENBQUM7QUFDRCxPO0FDVkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxnQkFBUSxvQkFBb0I7QUFDNUI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx5QkFBaUIsNEJBQTRCO0FBQzdDO0FBQ0E7QUFDQSwwQkFBa0IsMkJBQTJCO0FBQzdDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7OztBQUdBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxrREFBMEMsZ0NBQWdDO0FBQzFFO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0VBQXdELGtCQUFrQjtBQUMxRTtBQUNB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RUFBRUMsUUFBaEM7QUFBMEMsYUFBSyxFQUFFa0g7QUFBakQsU0FDS2hILFFBREwsQ0FESjtBQUtIOzs7O0VBbEIrQk0sNENBQUssQ0FBQ0MsUzs7O0FBcUIxQ3FHLE1BQU0sQ0FBQ3BHLFlBQVAsR0FBc0IsRUFBdEIsQyxDQUVBOztBQUVBb0csTUFBTSxDQUFDbkcsU0FBUCxHQUFtQjtBQUNmVCxVQUFRLEVBQUVVLGlEQUFTLENBQUNDLElBREw7QUFFZmtHLEtBQUcsRUFBRW5HLGlEQUFTLENBQUNJLE1BRkE7QUFHZmtGLE1BQUksRUFBRXRGLGlEQUFTLENBQUNJLE1BSEQ7QUFJZmdHLE9BQUssRUFBRXBHLGlEQUFTLENBQUNJLE1BSkY7QUFLZmlHLFFBQU0sRUFBRXJHLGlEQUFTLENBQUNJLE1BTEg7QUFPZmpCLFlBQVUsRUFBRWEsaURBQVMsQ0FBQ0ksTUFQUDtBQVFmZixPQUFLLEVBQUVXLGlEQUFTLENBQUNHLE1BUkY7QUFTZmYsVUFBUSxFQUFFWSxpREFBUyxDQUFDSTtBQVRMLENBQW5CLEM7Ozs7Ozs7Ozs7OztBQ2hDQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7Ozs7Ozs7OztBQ05BLGNBQWMsbUJBQU8sQ0FBQyxpVkFBMEs7O0FBRWhNLDRDQUE0QyxRQUFTOztBQUVyRDtBQUNBOzs7O0FBSUEsZUFBZTs7QUFFZjtBQUNBOztBQUVBLGFBQWEsbUJBQU8sQ0FBQyx5R0FBc0Q7O0FBRTNFOztBQUVBLEdBQUcsS0FBVSxFQUFFLEU7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDbkJmLG1EIiwiZmlsZSI6ImRhenpsZXJfZXh0cmFfMzk1YjQxZWZiNGMwOWYyNWI5YzcuanMiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2V4dHJhXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfZXh0cmFcIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KSh3aW5kb3csIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsIiBcdC8vIGluc3RhbGwgYSBKU09OUCBjYWxsYmFjayBmb3IgY2h1bmsgbG9hZGluZ1xuIFx0ZnVuY3Rpb24gd2VicGFja0pzb25wQ2FsbGJhY2soZGF0YSkge1xuIFx0XHR2YXIgY2h1bmtJZHMgPSBkYXRhWzBdO1xuIFx0XHR2YXIgbW9yZU1vZHVsZXMgPSBkYXRhWzFdO1xuIFx0XHR2YXIgZXhlY3V0ZU1vZHVsZXMgPSBkYXRhWzJdO1xuXG4gXHRcdC8vIGFkZCBcIm1vcmVNb2R1bGVzXCIgdG8gdGhlIG1vZHVsZXMgb2JqZWN0LFxuIFx0XHQvLyB0aGVuIGZsYWcgYWxsIFwiY2h1bmtJZHNcIiBhcyBsb2FkZWQgYW5kIGZpcmUgY2FsbGJhY2tcbiBcdFx0dmFyIG1vZHVsZUlkLCBjaHVua0lkLCBpID0gMCwgcmVzb2x2ZXMgPSBbXTtcbiBcdFx0Zm9yKDtpIDwgY2h1bmtJZHMubGVuZ3RoOyBpKyspIHtcbiBcdFx0XHRjaHVua0lkID0gY2h1bmtJZHNbaV07XG4gXHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdKSB7XG4gXHRcdFx0XHRyZXNvbHZlcy5wdXNoKGluc3RhbGxlZENodW5rc1tjaHVua0lkXVswXSk7XG4gXHRcdFx0fVxuIFx0XHRcdGluc3RhbGxlZENodW5rc1tjaHVua0lkXSA9IDA7XG4gXHRcdH1cbiBcdFx0Zm9yKG1vZHVsZUlkIGluIG1vcmVNb2R1bGVzKSB7XG4gXHRcdFx0aWYoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG1vcmVNb2R1bGVzLCBtb2R1bGVJZCkpIHtcbiBcdFx0XHRcdG1vZHVsZXNbbW9kdWxlSWRdID0gbW9yZU1vZHVsZXNbbW9kdWxlSWRdO1xuIFx0XHRcdH1cbiBcdFx0fVxuIFx0XHRpZihwYXJlbnRKc29ucEZ1bmN0aW9uKSBwYXJlbnRKc29ucEZ1bmN0aW9uKGRhdGEpO1xuXG4gXHRcdHdoaWxlKHJlc29sdmVzLmxlbmd0aCkge1xuIFx0XHRcdHJlc29sdmVzLnNoaWZ0KCkoKTtcbiBcdFx0fVxuXG4gXHRcdC8vIGFkZCBlbnRyeSBtb2R1bGVzIGZyb20gbG9hZGVkIGNodW5rIHRvIGRlZmVycmVkIGxpc3RcbiBcdFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2guYXBwbHkoZGVmZXJyZWRNb2R1bGVzLCBleGVjdXRlTW9kdWxlcyB8fCBbXSk7XG5cbiBcdFx0Ly8gcnVuIGRlZmVycmVkIG1vZHVsZXMgd2hlbiBhbGwgY2h1bmtzIHJlYWR5XG4gXHRcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIFx0fTtcbiBcdGZ1bmN0aW9uIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCkge1xuIFx0XHR2YXIgcmVzdWx0O1xuIFx0XHRmb3IodmFyIGkgPSAwOyBpIDwgZGVmZXJyZWRNb2R1bGVzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0dmFyIGRlZmVycmVkTW9kdWxlID0gZGVmZXJyZWRNb2R1bGVzW2ldO1xuIFx0XHRcdHZhciBmdWxmaWxsZWQgPSB0cnVlO1xuIFx0XHRcdGZvcih2YXIgaiA9IDE7IGogPCBkZWZlcnJlZE1vZHVsZS5sZW5ndGg7IGorKykge1xuIFx0XHRcdFx0dmFyIGRlcElkID0gZGVmZXJyZWRNb2R1bGVbal07XG4gXHRcdFx0XHRpZihpbnN0YWxsZWRDaHVua3NbZGVwSWRdICE9PSAwKSBmdWxmaWxsZWQgPSBmYWxzZTtcbiBcdFx0XHR9XG4gXHRcdFx0aWYoZnVsZmlsbGVkKSB7XG4gXHRcdFx0XHRkZWZlcnJlZE1vZHVsZXMuc3BsaWNlKGktLSwgMSk7XG4gXHRcdFx0XHRyZXN1bHQgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IGRlZmVycmVkTW9kdWxlWzBdKTtcbiBcdFx0XHR9XG4gXHRcdH1cblxuIFx0XHRyZXR1cm4gcmVzdWx0O1xuIFx0fVxuXG4gXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBvYmplY3QgdG8gc3RvcmUgbG9hZGVkIGFuZCBsb2FkaW5nIGNodW5rc1xuIFx0Ly8gdW5kZWZpbmVkID0gY2h1bmsgbm90IGxvYWRlZCwgbnVsbCA9IGNodW5rIHByZWxvYWRlZC9wcmVmZXRjaGVkXG4gXHQvLyBQcm9taXNlID0gY2h1bmsgbG9hZGluZywgMCA9IGNodW5rIGxvYWRlZFxuIFx0dmFyIGluc3RhbGxlZENodW5rcyA9IHtcbiBcdFx0XCJleHRyYVwiOiAwXG4gXHR9O1xuXG4gXHR2YXIgZGVmZXJyZWRNb2R1bGVzID0gW107XG5cbiBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4gXHRmdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cbiBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4gXHRcdGlmKGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdKSB7XG4gXHRcdFx0cmV0dXJuIGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdLmV4cG9ydHM7XG4gXHRcdH1cbiBcdFx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcbiBcdFx0dmFyIG1vZHVsZSA9IGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdID0ge1xuIFx0XHRcdGk6IG1vZHVsZUlkLFxuIFx0XHRcdGw6IGZhbHNlLFxuIFx0XHRcdGV4cG9ydHM6IHt9XG4gXHRcdH07XG5cbiBcdFx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG4gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG4gXHRcdC8vIEZsYWcgdGhlIG1vZHVsZSBhcyBsb2FkZWRcbiBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuXG4gXHRcdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG4gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbiBcdH1cblxuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZXMgb2JqZWN0IChfX3dlYnBhY2tfbW9kdWxlc19fKVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5tID0gbW9kdWxlcztcblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGUgY2FjaGVcbiBcdF9fd2VicGFja19yZXF1aXJlX18uYyA9IGluc3RhbGxlZE1vZHVsZXM7XG5cbiBcdC8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb24gZm9yIGhhcm1vbnkgZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4gXHRcdGlmKCFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywgbmFtZSkpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgbmFtZSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGdldHRlciB9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZGVmaW5lIF9fZXNNb2R1bGUgb24gZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yID0gZnVuY3Rpb24oZXhwb3J0cykge1xuIFx0XHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcbiBcdFx0fVxuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xuIFx0fTtcblxuIFx0Ly8gY3JlYXRlIGEgZmFrZSBuYW1lc3BhY2Ugb2JqZWN0XG4gXHQvLyBtb2RlICYgMTogdmFsdWUgaXMgYSBtb2R1bGUgaWQsIHJlcXVpcmUgaXRcbiBcdC8vIG1vZGUgJiAyOiBtZXJnZSBhbGwgcHJvcGVydGllcyBvZiB2YWx1ZSBpbnRvIHRoZSBuc1xuIFx0Ly8gbW9kZSAmIDQ6IHJldHVybiB2YWx1ZSB3aGVuIGFscmVhZHkgbnMgb2JqZWN0XG4gXHQvLyBtb2RlICYgOHwxOiBiZWhhdmUgbGlrZSByZXF1aXJlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnQgPSBmdW5jdGlvbih2YWx1ZSwgbW9kZSkge1xuIFx0XHRpZihtb2RlICYgMSkgdmFsdWUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKHZhbHVlKTtcbiBcdFx0aWYobW9kZSAmIDgpIHJldHVybiB2YWx1ZTtcbiBcdFx0aWYoKG1vZGUgJiA0KSAmJiB0eXBlb2YgdmFsdWUgPT09ICdvYmplY3QnICYmIHZhbHVlICYmIHZhbHVlLl9fZXNNb2R1bGUpIHJldHVybiB2YWx1ZTtcbiBcdFx0dmFyIG5zID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yKG5zKTtcbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KG5zLCAnZGVmYXVsdCcsIHsgZW51bWVyYWJsZTogdHJ1ZSwgdmFsdWU6IHZhbHVlIH0pO1xuIFx0XHRpZihtb2RlICYgMiAmJiB0eXBlb2YgdmFsdWUgIT0gJ3N0cmluZycpIGZvcih2YXIga2V5IGluIHZhbHVlKSBfX3dlYnBhY2tfcmVxdWlyZV9fLmQobnMsIGtleSwgZnVuY3Rpb24oa2V5KSB7IHJldHVybiB2YWx1ZVtrZXldOyB9LmJpbmQobnVsbCwga2V5KSk7XG4gXHRcdHJldHVybiBucztcbiBcdH07XG5cbiBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm4gPSBmdW5jdGlvbihtb2R1bGUpIHtcbiBcdFx0dmFyIGdldHRlciA9IG1vZHVsZSAmJiBtb2R1bGUuX19lc01vZHVsZSA/XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbiBcdFx0XHRmdW5jdGlvbiBnZXRNb2R1bGVFeHBvcnRzKCkgeyByZXR1cm4gbW9kdWxlOyB9O1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQoZ2V0dGVyLCAnYScsIGdldHRlcik7XG4gXHRcdHJldHVybiBnZXR0ZXI7XG4gXHR9O1xuXG4gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubyA9IGZ1bmN0aW9uKG9iamVjdCwgcHJvcGVydHkpIHsgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsIHByb3BlcnR5KTsgfTtcblxuIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbiBcdF9fd2VicGFja19yZXF1aXJlX18ucCA9IFwiXCI7XG5cbiBcdHZhciBqc29ucEFycmF5ID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSA9IHdpbmRvd1tcIndlYnBhY2tKc29ucGRhenpsZXJfbmFtZV9cIl0gfHwgW107XG4gXHR2YXIgb2xkSnNvbnBGdW5jdGlvbiA9IGpzb25wQXJyYXkucHVzaC5iaW5kKGpzb25wQXJyYXkpO1xuIFx0anNvbnBBcnJheS5wdXNoID0gd2VicGFja0pzb25wQ2FsbGJhY2s7XG4gXHRqc29ucEFycmF5ID0ganNvbnBBcnJheS5zbGljZSgpO1xuIFx0Zm9yKHZhciBpID0gMDsgaSA8IGpzb25wQXJyYXkubGVuZ3RoOyBpKyspIHdlYnBhY2tKc29ucENhbGxiYWNrKGpzb25wQXJyYXlbaV0pO1xuIFx0dmFyIHBhcmVudEpzb25wRnVuY3Rpb24gPSBvbGRKc29ucEZ1bmN0aW9uO1xuXG5cbiBcdC8vIGFkZCBlbnRyeSBtb2R1bGUgdG8gZGVmZXJyZWQgbGlzdFxuIFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2goWzQsXCJjb21tb25zXCJdKTtcbiBcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gcmVhZHlcbiBcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIiwiLy8gZXh0cmFjdGVkIGJ5IG1pbmktY3NzLWV4dHJhY3QtcGx1Z2luIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge2pvaW4sIGNvbmNhdH0gZnJvbSAncmFtZGEnO1xuXG5jb25zdCBDYXJldCA9ICh7c2lkZSwgb3BlbmVkfSkgPT4ge1xuICAgIHN3aXRjaCAoc2lkZSkge1xuICAgICAgICBjYXNlICd0b3AnOlxuICAgICAgICAgICAgcmV0dXJuIG9wZW5lZCA/IDxzcGFuPiYjOTY1MDs8L3NwYW4+IDogPHNwYW4+JiM5NjYwOzwvc3Bhbj47XG4gICAgICAgIGNhc2UgJ3JpZ2h0JzpcbiAgICAgICAgICAgIHJldHVybiBvcGVuZWQgPyA8c3Bhbj4mIzk2NTY7PC9zcGFuPiA6IDxzcGFuPiYjOTY2Njs8L3NwYW4+O1xuICAgICAgICBjYXNlICdsZWZ0JzpcbiAgICAgICAgICAgIHJldHVybiBvcGVuZWQgPyA8c3Bhbj4mIzk2NjY7PC9zcGFuPiA6IDxzcGFuPiYjOTY1Njs8L3NwYW4+O1xuICAgICAgICBjYXNlICdib3R0b20nOlxuICAgICAgICAgICAgcmV0dXJuIG9wZW5lZCA/IDxzcGFuPiYjOTY2MDs8L3NwYW4+IDogPHNwYW4+JiM5NjUwOzwvc3Bhbj47XG4gICAgfVxufTtcblxuLyoqXG4gKiBEcmF3IGNvbnRlbnQgZnJvbSB0aGUgc2lkZXMgb2YgdGhlIHNjcmVlbi5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgRHJhd2VyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtcbiAgICAgICAgICAgIGNsYXNzX25hbWUsXG4gICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgIHN0eWxlLFxuICAgICAgICAgICAgY2hpbGRyZW4sXG4gICAgICAgICAgICBvcGVuZWQsXG4gICAgICAgICAgICBzaWRlLFxuICAgICAgICB9ID0gdGhpcy5wcm9wcztcblxuICAgICAgICBjb25zdCBjc3MgPSBbc2lkZV07XG5cbiAgICAgICAgaWYgKHNpZGUgPT09ICd0b3AnIHx8IHNpZGUgPT09ICdib3R0b20nKSB7XG4gICAgICAgICAgICBjc3MucHVzaCgnaG9yaXpvbnRhbCcpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgY3NzLnB1c2goJ3ZlcnRpY2FsJyk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17am9pbignICcsIGNvbmNhdChjc3MsIFtjbGFzc19uYW1lXSkpfVxuICAgICAgICAgICAgICAgIGlkPXtpZGVudGl0eX1cbiAgICAgICAgICAgICAgICBzdHlsZT17c3R5bGV9XG4gICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAge29wZW5lZCAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPXtqb2luKCcgJywgY29uY2F0KGNzcywgWydkcmF3ZXItY29udGVudCddKSl9PlxuICAgICAgICAgICAgICAgICAgICAgICAge2NoaWxkcmVufVxuICAgICAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPXtqb2luKCcgJywgY29uY2F0KGNzcywgWydkcmF3ZXItY29udHJvbCddKSl9XG4gICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9eygpID0+IHRoaXMucHJvcHMudXBkYXRlQXNwZWN0cyh7b3BlbmVkOiAhb3BlbmVkfSl9XG4gICAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgICAgICA8Q2FyZXQgb3BlbmVkPXtvcGVuZWR9IHNpZGU9e3NpZGV9IC8+XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICB9XG59XG5cbkRyYXdlci5kZWZhdWx0UHJvcHMgPSB7XG4gICAgc2lkZTogJ3RvcCcsXG59O1xuXG5EcmF3ZXIucHJvcFR5cGVzID0ge1xuICAgIGNoaWxkcmVuOiBQcm9wVHlwZXMubm9kZSxcbiAgICBvcGVuZWQ6IFByb3BUeXBlcy5ib29sLFxuICAgIHN0eWxlOiBQcm9wVHlwZXMub2JqZWN0LFxuICAgIGNsYXNzX25hbWU6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogU2lkZSB3aGljaCBvcGVuLlxuICAgICAqL1xuICAgIHNpZGU6IFByb3BUeXBlcy5vbmVPZihbJ3RvcCcsICdsZWZ0JywgJ3JpZ2h0JywgJ2JvdHRvbSddKSxcblxuICAgIC8qKlxuICAgICAqICBVbmlxdWUgaWQgZm9yIHRoaXMgY29tcG9uZW50XG4gICAgICovXG4gICAgaWRlbnRpdHk6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBVcGRhdGUgYXNwZWN0cyBvbiB0aGUgYmFja2VuZC5cbiAgICAgKi9cbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcbmltcG9ydCB7dGltZXN0YW1wUHJvcH0gZnJvbSAnY29tbW9ucyc7XG5pbXBvcnQge21lcmdlfSBmcm9tICdyYW1kYSc7XG5cbi8qKlxuICogQnJvd3NlciBub3RpZmljYXRpb25zIHdpdGggcGVybWlzc2lvbnMgaGFuZGxpbmcuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIE5vdGljZSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgbGFzdE1lc3NhZ2U6IHByb3BzLmJvZHksXG4gICAgICAgICAgICBub3RpZmljYXRpb246IG51bGwsXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMub25QZXJtaXNzaW9uID0gdGhpcy5vblBlcm1pc3Npb24uYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgY29uc3Qge3VwZGF0ZUFzcGVjdHN9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgaWYgKCEoJ05vdGlmaWNhdGlvbicgaW4gd2luZG93KSAmJiB1cGRhdGVBc3BlY3RzKSB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHtwZXJtaXNzaW9uOiAndW5zdXBwb3J0ZWQnfSk7XG4gICAgICAgIH0gZWxzZSBpZiAoTm90aWZpY2F0aW9uLnBlcm1pc3Npb24gPT09ICdkZWZhdWx0Jykge1xuICAgICAgICAgICAgTm90aWZpY2F0aW9uLnJlcXVlc3RQZXJtaXNzaW9uKCkudGhlbih0aGlzLm9uUGVybWlzc2lvbik7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLm9uUGVybWlzc2lvbih3aW5kb3cuTm90aWZpY2F0aW9uLnBlcm1pc3Npb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgY29tcG9uZW50RGlkVXBkYXRlKHByZXZQcm9wcykge1xuICAgICAgICBpZiAoIXByZXZQcm9wcy5kaXNwbGF5ZWQgJiYgdGhpcy5wcm9wcy5kaXNwbGF5ZWQpIHtcbiAgICAgICAgICAgIHRoaXMuc2VuZE5vdGlmaWNhdGlvbih0aGlzLnByb3BzLnBlcm1pc3Npb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgc2VuZE5vdGlmaWNhdGlvbihwZXJtaXNzaW9uKSB7XG4gICAgICAgIGNvbnN0IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICBib2R5LFxuICAgICAgICAgICAgdGl0bGUsXG4gICAgICAgICAgICBpY29uLFxuICAgICAgICAgICAgcmVxdWlyZV9pbnRlcmFjdGlvbixcbiAgICAgICAgICAgIGxhbmcsXG4gICAgICAgICAgICBiYWRnZSxcbiAgICAgICAgICAgIHRhZyxcbiAgICAgICAgICAgIGltYWdlLFxuICAgICAgICAgICAgdmlicmF0ZSxcbiAgICAgICAgfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGlmIChwZXJtaXNzaW9uID09PSAnZ3JhbnRlZCcpIHtcbiAgICAgICAgICAgIGNvbnN0IG9wdGlvbnMgPSB7XG4gICAgICAgICAgICAgICAgcmVxdWlyZUludGVyYWN0aW9uOiByZXF1aXJlX2ludGVyYWN0aW9uLFxuICAgICAgICAgICAgICAgIGJvZHksXG4gICAgICAgICAgICAgICAgaWNvbixcbiAgICAgICAgICAgICAgICBsYW5nLFxuICAgICAgICAgICAgICAgIGJhZGdlLFxuICAgICAgICAgICAgICAgIHRhZyxcbiAgICAgICAgICAgICAgICBpbWFnZSxcbiAgICAgICAgICAgICAgICB2aWJyYXRlLFxuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIGNvbnN0IG5vdGlmaWNhdGlvbiA9IG5ldyBOb3RpZmljYXRpb24odGl0bGUsIG9wdGlvbnMpO1xuICAgICAgICAgICAgbm90aWZpY2F0aW9uLm9uY2xpY2sgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIG1lcmdlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtkaXNwbGF5ZWQ6IGZhbHNlfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aW1lc3RhbXBQcm9wKCdjbGlja3MnLCB0aGlzLnByb3BzLmNsaWNrcyArIDEpXG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIG5vdGlmaWNhdGlvbi5vbmNsb3NlID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgIGlmICh1cGRhdGVBc3BlY3RzKSB7XG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoXG4gICAgICAgICAgICAgICAgICAgICAgICBtZXJnZShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7ZGlzcGxheWVkOiBmYWxzZX0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGltZXN0YW1wUHJvcCgnY2xvc2VzJywgdGhpcy5wcm9wcy5jbG9zZXMgKyAxKVxuICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH07XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBvblBlcm1pc3Npb24ocGVybWlzc2lvbikge1xuICAgICAgICBjb25zdCB7ZGlzcGxheWVkLCB1cGRhdGVBc3BlY3RzfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGlmICh1cGRhdGVBc3BlY3RzKSB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHtwZXJtaXNzaW9ufSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRpc3BsYXllZCkge1xuICAgICAgICAgICAgdGhpcy5zZW5kTm90aWZpY2F0aW9uKHBlcm1pc3Npb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG59XG5cbk5vdGljZS5kZWZhdWx0UHJvcHMgPSB7XG4gICAgcmVxdWlyZV9pbnRlcmFjdGlvbjogZmFsc2UsXG4gICAgY2xpY2tzOiAwLFxuICAgIGNsaWNrc190aW1lc3RhbXA6IC0xLFxuICAgIGNsb3NlczogMCxcbiAgICBjbG9zZXNfdGltZXN0YW1wOiAtMSxcbn07XG5cbi8vIFByb3BzIGRvY3MgZnJvbSBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9BUEkvTm90aWZpY2F0aW9uL05vdGlmaWNhdGlvblxuTm90aWNlLnByb3BUeXBlcyA9IHtcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIC8qKlxuICAgICAqIFBlcm1pc3Npb24gZ3JhbnRlZCBieSB0aGUgdXNlciAoUkVBRE9OTFkpXG4gICAgICovXG4gICAgcGVybWlzc2lvbjogUHJvcFR5cGVzLm9uZU9mKFtcbiAgICAgICAgJ2RlbmllZCcsXG4gICAgICAgICdncmFudGVkJyxcbiAgICAgICAgJ2RlZmF1bHQnLFxuICAgICAgICAndW5zdXBwb3J0ZWQnLFxuICAgIF0pLFxuXG4gICAgdGl0bGU6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcblxuICAgIC8qKlxuICAgICAqIFRoZSBub3RpZmljYXRpb24ncyBsYW5ndWFnZSwgYXMgc3BlY2lmaWVkIHVzaW5nIGEgRE9NU3RyaW5nIHJlcHJlc2VudGluZyBhIEJDUCA0NyBsYW5ndWFnZSB0YWcuXG4gICAgICovXG4gICAgbGFuZzogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBBIERPTVN0cmluZyByZXByZXNlbnRpbmcgdGhlIGJvZHkgdGV4dCBvZiB0aGUgbm90aWZpY2F0aW9uLCB3aGljaCB3aWxsIGJlIGRpc3BsYXllZCBiZWxvdyB0aGUgdGl0bGUuXG4gICAgICovXG4gICAgYm9keTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBBIFVTVlN0cmluZyBjb250YWluaW5nIHRoZSBVUkwgb2YgdGhlIGltYWdlIHVzZWQgdG8gcmVwcmVzZW50IHRoZSBub3RpZmljYXRpb24gd2hlbiB0aGVyZSBpcyBub3QgZW5vdWdoIHNwYWNlIHRvIGRpc3BsYXkgdGhlIG5vdGlmaWNhdGlvbiBpdHNlbGYuXG4gICAgICovXG4gICAgYmFkZ2U6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBBIERPTVN0cmluZyByZXByZXNlbnRpbmcgYW4gaWRlbnRpZnlpbmcgdGFnIGZvciB0aGUgbm90aWZpY2F0aW9uLlxuICAgICAqL1xuICAgIHRhZzogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBBIFVTVlN0cmluZyBjb250YWluaW5nIHRoZSBVUkwgb2YgYW4gaWNvbiB0byBiZSBkaXNwbGF5ZWQgaW4gdGhlIG5vdGlmaWNhdGlvbi5cbiAgICAgKi9cbiAgICBpY29uOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqICBhIFVTVlN0cmluZyBjb250YWluaW5nIHRoZSBVUkwgb2YgYW4gaW1hZ2UgdG8gYmUgZGlzcGxheWVkIGluIHRoZSBub3RpZmljYXRpb24uXG4gICAgICovXG4gICAgaW1hZ2U6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogQSB2aWJyYXRpb24gcGF0dGVybiBmb3IgdGhlIGRldmljZSdzIHZpYnJhdGlvbiBoYXJkd2FyZSB0byBlbWl0IHdoZW4gdGhlIG5vdGlmaWNhdGlvbiBmaXJlcy5cbiAgICAgKi9cbiAgICB2aWJyYXRlOiBQcm9wVHlwZXMub25lT2ZUeXBlKFtcbiAgICAgICAgUHJvcFR5cGVzLm51bWJlcixcbiAgICAgICAgUHJvcFR5cGVzLmFycmF5T2YoUHJvcFR5cGVzLm51bWJlciksXG4gICAgXSksXG4gICAgLyoqXG4gICAgICogSW5kaWNhdGVzIHRoYXQgYSBub3RpZmljYXRpb24gc2hvdWxkIHJlbWFpbiBhY3RpdmUgdW50aWwgdGhlIHVzZXIgY2xpY2tzIG9yIGRpc21pc3NlcyBpdCwgcmF0aGVyIHRoYW4gY2xvc2luZyBhdXRvbWF0aWNhbGx5LiBUaGUgZGVmYXVsdCB2YWx1ZSBpcyBmYWxzZS5cbiAgICAgKi9cbiAgICByZXF1aXJlX2ludGVyYWN0aW9uOiBQcm9wVHlwZXMuYm9vbCxcblxuICAgIC8qKlxuICAgICAqIFNldCB0byB0cnVlIHRvIGRpc3BsYXkgdGhlIG5vdGlmaWNhdGlvbi5cbiAgICAgKi9cbiAgICBkaXNwbGF5ZWQ6IFByb3BUeXBlcy5ib29sLFxuXG4gICAgY2xpY2tzOiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIGNsaWNrc190aW1lc3RhbXA6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgLyoqXG4gICAgICogTnVtYmVyIG9mIHRpbWVzIHRoZSBub3RpZmljYXRpb24gd2FzIGNsb3NlZC5cbiAgICAgKi9cbiAgICBjbG9zZXM6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgY2xvc2VzX3RpbWVzdGFtcDogUHJvcFR5cGVzLm51bWJlcixcblxuICAgIHVwZGF0ZUFzcGVjdDogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge3JhbmdlLCBqb2lufSBmcm9tICdyYW1kYSc7XG5cbmNvbnN0IHN0YXJ0T2Zmc2V0ID0gKHBhZ2UsIGl0ZW1QZXJQYWdlKSA9PlxuICAgIChwYWdlIC0gMSkgKiAocGFnZSA+IDEgPyBpdGVtUGVyUGFnZSA6IDApO1xuXG5jb25zdCBlbmRPZmZzZXQgPSAoc3RhcnQsIGl0ZW1QZXJQYWdlLCBwYWdlLCB0b3RhbCwgbGVmdE92ZXIpID0+XG4gICAgcGFnZSAhPT0gdG90YWxcbiAgICAgICAgPyBzdGFydCArIGl0ZW1QZXJQYWdlXG4gICAgICAgIDogbGVmdE92ZXIgIT09IDBcbiAgICAgICAgPyBzdGFydCArIGxlZnRPdmVyXG4gICAgICAgIDogc3RhcnQgKyBpdGVtUGVyUGFnZTtcblxuY29uc3Qgc2hvd0xpc3QgPSAocGFnZSwgdG90YWwsIG4pID0+IHtcbiAgICBpZiAodG90YWwgPiBuKSB7XG4gICAgICAgIGNvbnN0IG1pZGRsZSA9IG4gLyAyO1xuICAgICAgICBjb25zdCBmaXJzdCA9XG4gICAgICAgICAgICBwYWdlID49IHRvdGFsIC0gbWlkZGxlXG4gICAgICAgICAgICAgICAgPyB0b3RhbCAtIG4gKyAxXG4gICAgICAgICAgICAgICAgOiBwYWdlID4gbWlkZGxlXG4gICAgICAgICAgICAgICAgPyBwYWdlIC0gbWlkZGxlXG4gICAgICAgICAgICAgICAgOiAxO1xuICAgICAgICBjb25zdCBsYXN0ID0gcGFnZSA8IHRvdGFsIC0gbWlkZGxlID8gZmlyc3QgKyBuIDogdG90YWwgKyAxO1xuICAgICAgICByZXR1cm4gcmFuZ2UoZmlyc3QsIGxhc3QpO1xuICAgIH1cbiAgICByZXR1cm4gcmFuZ2UoMSwgdG90YWwgKyAxKTtcbn07XG5cbmNvbnN0IFBhZ2UgPSAoe3N0eWxlLCBjbGFzc19uYW1lLCBvbl9jaGFuZ2UsIHRleHQsIHBhZ2V9KSA9PiAoXG4gICAgPHNwYW4gc3R5bGU9e3N0eWxlfSBjbGFzc05hbWU9e2NsYXNzX25hbWV9IG9uQ2xpY2s9eygpID0+IG9uX2NoYW5nZShwYWdlKX0+XG4gICAgICAgIHt0ZXh0IHx8IHBhZ2V9XG4gICAgPC9zcGFuPlxuKTtcblxuLyoqXG4gKiBQYWdpbmcgZm9yIGRhenpsZXIgYXBwcy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgUGFnZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIGN1cnJlbnRfcGFnZTogbnVsbCxcbiAgICAgICAgICAgIHN0YXJ0X29mZnNldDogbnVsbCxcbiAgICAgICAgICAgIGVuZF9vZmZzZXQ6IG51bGwsXG4gICAgICAgICAgICBwYWdlczogW10sXG4gICAgICAgICAgICB0b3RhbF9wYWdlczogTWF0aC5jZWlsKHByb3BzLnRvdGFsX2l0ZW1zIC8gcHJvcHMuaXRlbXNfcGVyX3BhZ2UpLFxuICAgICAgICB9O1xuICAgICAgICB0aGlzLm9uQ2hhbmdlUGFnZSA9IHRoaXMub25DaGFuZ2VQYWdlLmJpbmQodGhpcyk7XG4gICAgfVxuXG4gICAgY29tcG9uZW50V2lsbE1vdW50KCkge1xuICAgICAgICB0aGlzLm9uQ2hhbmdlUGFnZSh0aGlzLnByb3BzLmN1cnJlbnRfcGFnZSk7XG4gICAgfVxuXG4gICAgb25DaGFuZ2VQYWdlKHBhZ2UpIHtcbiAgICAgICAgY29uc3Qge1xuICAgICAgICAgICAgaXRlbXNfcGVyX3BhZ2UsXG4gICAgICAgICAgICB0b3RhbF9pdGVtcyxcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICBwYWdlc19kaXNwbGF5ZWQsXG4gICAgICAgIH0gPSB0aGlzLnByb3BzO1xuICAgICAgICBjb25zdCB7dG90YWxfcGFnZXN9ID0gdGhpcy5zdGF0ZTtcblxuICAgICAgICBjb25zdCBzdGFydF9vZmZzZXQgPSBzdGFydE9mZnNldChwYWdlLCBpdGVtc19wZXJfcGFnZSk7XG4gICAgICAgIGNvbnN0IGxlZnRPdmVyID0gdG90YWxfaXRlbXMgJSBpdGVtc19wZXJfcGFnZTtcblxuICAgICAgICBjb25zdCBlbmRfb2Zmc2V0ID0gZW5kT2Zmc2V0KFxuICAgICAgICAgICAgc3RhcnRfb2Zmc2V0LFxuICAgICAgICAgICAgaXRlbXNfcGVyX3BhZ2UsXG4gICAgICAgICAgICBwYWdlLFxuICAgICAgICAgICAgdG90YWxfcGFnZXMsXG4gICAgICAgICAgICBsZWZ0T3ZlclxuICAgICAgICApO1xuXG4gICAgICAgIGNvbnN0IHBheWxvYWQgPSB7XG4gICAgICAgICAgICBjdXJyZW50X3BhZ2U6IHBhZ2UsXG4gICAgICAgICAgICBzdGFydF9vZmZzZXQ6IHN0YXJ0X29mZnNldCxcbiAgICAgICAgICAgIGVuZF9vZmZzZXQ6IGVuZF9vZmZzZXQsXG4gICAgICAgICAgICBwYWdlczogc2hvd0xpc3QocGFnZSwgdG90YWxfcGFnZXMsIHBhZ2VzX2Rpc3BsYXllZCksXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMuc2V0U3RhdGUocGF5bG9hZCk7XG5cbiAgICAgICAgaWYgKHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgICAgIGlmICh0aGlzLnN0YXRlLnRvdGFsX3BhZ2VzICE9PSB0aGlzLnByb3BzLnRvdGFsX3BhZ2VzKSB7XG4gICAgICAgICAgICAgICAgcGF5bG9hZC50b3RhbF9wYWdlcyA9IHRoaXMuc3RhdGUudG90YWxfcGFnZXM7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHBheWxvYWQpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgY29tcG9uZW50V2lsbFJlY2VpdmVQcm9wcyhwcm9wcykge1xuICAgICAgICBpZiAocHJvcHMuY3VycmVudF9wYWdlICE9PSB0aGlzLnN0YXRlLmN1cnJlbnRfcGFnZSkge1xuICAgICAgICAgICAgdGhpcy5vbkNoYW5nZVBhZ2UocHJvcHMuY3VycmVudF9wYWdlKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge2N1cnJlbnRfcGFnZSwgcGFnZXMsIHRvdGFsX3BhZ2VzfSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGNvbnN0IHtjbGFzc19uYW1lLCBpZGVudGl0eSwgcGFnZV9zdHlsZSwgcGFnZV9jbGFzc19uYW1lfSA9IHRoaXMucHJvcHM7XG5cbiAgICAgICAgbGV0IHBhZ2VDc3MgPSBbJ3BhZ2UnXTtcbiAgICAgICAgaWYgKHBhZ2VfY2xhc3NfbmFtZSkge1xuICAgICAgICAgICAgcGFnZUNzcy5wdXNoKHBhZ2VfY2xhc3NfbmFtZSk7XG4gICAgICAgIH1cbiAgICAgICAgcGFnZUNzcyA9IGpvaW4oJyAnLCBwYWdlQ3NzKTtcblxuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IGlkPXtpZGVudGl0eX0+XG4gICAgICAgICAgICAgICAge2N1cnJlbnRfcGFnZSA+IDEgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17MX1cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eydmaXJzdCd9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAge2N1cnJlbnRfcGFnZSA+IDEgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17Y3VycmVudF9wYWdlIC0gMX1cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eydwcmV2aW91cyd9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAge3BhZ2VzLm1hcChlID0+IChcbiAgICAgICAgICAgICAgICAgICAgPFBhZ2VcbiAgICAgICAgICAgICAgICAgICAgICAgIHBhZ2U9e2V9XG4gICAgICAgICAgICAgICAgICAgICAgICBrZXk9e2BwYWdlLSR7ZX1gfVxuICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGU9e3BhZ2Vfc3R5bGV9XG4gICAgICAgICAgICAgICAgICAgICAgICBjbGFzc19uYW1lPXtwYWdlQ3NzfVxuICAgICAgICAgICAgICAgICAgICAgICAgb25fY2hhbmdlPXt0aGlzLm9uQ2hhbmdlUGFnZX1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICApKX1cbiAgICAgICAgICAgICAgICB7Y3VycmVudF9wYWdlIDwgdG90YWxfcGFnZXMgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17Y3VycmVudF9wYWdlICsgMX1cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eyduZXh0J31cbiAgICAgICAgICAgICAgICAgICAgICAgIHN0eWxlPXtwYWdlX3N0eWxlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NfbmFtZT17cGFnZUNzc31cbiAgICAgICAgICAgICAgICAgICAgICAgIG9uX2NoYW5nZT17dGhpcy5vbkNoYW5nZVBhZ2V9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgICB7Y3VycmVudF9wYWdlIDwgdG90YWxfcGFnZXMgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17dG90YWxfcGFnZXN9XG4gICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PXsnbGFzdCd9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICB9XG59XG5cblBhZ2VyLmRlZmF1bHRQcm9wcyA9IHtcbiAgICBjdXJyZW50X3BhZ2U6IDEsXG4gICAgaXRlbXNfcGVyX3BhZ2U6IDEwLFxuICAgIHBhZ2VzX2Rpc3BsYXllZDogMTAsXG59O1xuXG5QYWdlci5wcm9wVHlwZXMgPSB7XG4gICAgLyoqXG4gICAgICogVGhlIHRvdGFsIGl0ZW1zIGluIHRoZSBzZXQuXG4gICAgICovXG4gICAgdG90YWxfaXRlbXM6IFByb3BUeXBlcy5udW1iZXIuaXNSZXF1aXJlZCxcbiAgICAvKipcbiAgICAgKiBUaGUgbnVtYmVyIG9mIGl0ZW1zIGEgcGFnZSBjb250YWlucy5cbiAgICAgKi9cbiAgICBpdGVtc19wZXJfcGFnZTogUHJvcFR5cGVzLm51bWJlcixcblxuICAgIGlkZW50aXR5OiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIHN0eWxlOiBQcm9wVHlwZXMub2JqZWN0LFxuICAgIGNsYXNzX25hbWU6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogU3R5bGUgZm9yIHRoZSBwYWdlIG51bWJlcnMuXG4gICAgICovXG4gICAgcGFnZV9zdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICAvKipcbiAgICAgKiBDU1MgY2xhc3MgZm9yIHRoZSBwYWdlIG51bWJlcnMuXG4gICAgICovXG4gICAgcGFnZV9jbGFzc19uYW1lOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2YgcGFnZXMgZGlzcGxheWVkIGJ5IHRoZSBwYWdlci5cbiAgICAgKi9cbiAgICBwYWdlc19kaXNwbGF5ZWQ6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgLyoqXG4gICAgICogUmVhZCBvbmx5LCB0aGUgY3VycmVudGx5IGRpc3BsYXllZCBwYWdlcyBudW1iZXJzLlxuICAgICAqL1xuICAgIHBhZ2VzOiBQcm9wVHlwZXMuYXJyYXksXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgc2VsZWN0ZWQgcGFnZS5cbiAgICAgKi9cbiAgICBjdXJyZW50X3BhZ2U6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgLyoqXG4gICAgICogU2V0IGJ5IHRvdGFsX2l0ZW1zIC8gaXRlbXNfcGVyX3BhZ2VcbiAgICAgKi9cbiAgICB0b3RhbF9wYWdlczogUHJvcFR5cGVzLm51bWJlcixcblxuICAgIC8qKlxuICAgICAqIFRoZSBzdGFydGluZyBpbmRleCBvZiB0aGUgY3VycmVudCBwYWdlXG4gICAgICogQ2FuIGJlIHVzZWQgdG8gc2xpY2UgZGF0YSBlZzogZGF0YVtzdGFydF9vZmZzZXQ6IGVuZF9vZmZzZXRdXG4gICAgICovXG4gICAgc3RhcnRfb2Zmc2V0OiBQcm9wVHlwZXMubnVtYmVyLFxuICAgIC8qKlxuICAgICAqIFRoZSBlbmQgaW5kZXggb2YgdGhlIGN1cnJlbnQgcGFnZS5cbiAgICAgKi9cbiAgICBlbmRfb2Zmc2V0OiBQcm9wVHlwZXMubnVtYmVyLFxuXG4gICAgdXBkYXRlQXNwZWN0czogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5cbmZ1bmN0aW9uIGdldE1vdXNlWChlLCBwb3B1cCkge1xuICAgIHJldHVybiAoXG4gICAgICAgIGUuY2xpZW50WCAtXG4gICAgICAgIGUudGFyZ2V0LmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLmxlZnQgLVxuICAgICAgICBwb3B1cC5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS53aWR0aCAvIDJcbiAgICApO1xufVxuXG4vKipcbiAqIFdyYXBzIGEgY29tcG9uZW50L3RleHQgdG8gcmVuZGVyIGEgcG9wdXAgd2hlbiBob3ZlcmluZ1xuICogb3ZlciB0aGUgY2hpbGRyZW4gb3IgY2xpY2tpbmcgb24gaXQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFBvcFVwIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50IHtcbiAgICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgICAgICBzdXBlcihwcm9wcyk7XG4gICAgICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAgICAgICBwb3M6IG51bGwsXG4gICAgICAgIH07XG4gICAgfVxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge1xuICAgICAgICAgICAgY2xhc3NfbmFtZSxcbiAgICAgICAgICAgIHN0eWxlLFxuICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICBjaGlsZHJlbixcbiAgICAgICAgICAgIGNvbnRlbnQsXG4gICAgICAgICAgICBtb2RlLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgIGFjdGl2ZSxcbiAgICAgICAgICAgIGNvbnRlbnRfc3R5bGUsXG4gICAgICAgICAgICBjaGlsZHJlbl9zdHlsZSxcbiAgICAgICAgfSA9IHRoaXMucHJvcHM7XG5cbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPXtjbGFzc19uYW1lfSBzdHlsZT17c3R5bGV9IGlkPXtpZGVudGl0eX0+XG4gICAgICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9eydwb3B1cC1jb250ZW50JyArIChhY3RpdmUgPyAnIHZpc2libGUnIDogJycpfVxuICAgICAgICAgICAgICAgICAgICBzdHlsZT17e1xuICAgICAgICAgICAgICAgICAgICAgICAgLi4uKGNvbnRlbnRfc3R5bGUgfHwge30pLFxuICAgICAgICAgICAgICAgICAgICAgICAgbGVmdDogdGhpcy5zdGF0ZS5wb3MgfHwgMCxcbiAgICAgICAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgICAgICAgICAgcmVmPXtyID0+ICh0aGlzLnBvcHVwUmVmID0gcil9XG4gICAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgICAgICB7Y29udGVudH1cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cInBvcHVwLWNoaWxkcmVuXCJcbiAgICAgICAgICAgICAgICAgICAgb25Nb3VzZUVudGVyPXtlID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChtb2RlID09PSAnaG92ZXInKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3BvczogZ2V0TW91c2VYKGUsIHRoaXMucG9wdXBSZWYpfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgKCkgPT4gdXBkYXRlQXNwZWN0cyh7YWN0aXZlOiB0cnVlfSlcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgICAgICAgICBvbk1vdXNlTGVhdmU9eygpID0+XG4gICAgICAgICAgICAgICAgICAgICAgICBtb2RlID09PSAnaG92ZXInICYmIHVwZGF0ZUFzcGVjdHMoe2FjdGl2ZTogZmFsc2V9KVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9e2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKG1vZGUgPT09ICdjbGljaycpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7cG9zOiBnZXRNb3VzZVgoZSwgdGhpcy5wb3B1cFJlZil9LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAoKSA9PiB1cGRhdGVBc3BlY3RzKHthY3RpdmU6ICFhY3RpdmV9KVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIH19XG4gICAgICAgICAgICAgICAgICAgIHN0eWxlPXtjaGlsZHJlbl9zdHlsZX1cbiAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgIHtjaGlsZHJlbn1cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbn1cblxuUG9wVXAuZGVmYXVsdFByb3BzID0ge1xuICAgIG1vZGU6ICdob3ZlcicsXG4gICAgYWN0aXZlOiBmYWxzZSxcbn07XG5cblBvcFVwLnByb3BUeXBlcyA9IHtcbiAgICAvKipcbiAgICAgKiBDb21wb25lbnQvdGV4dCB0byB3cmFwIHdpdGggYSBwb3B1cCBvbiBob3Zlci9jbGljay5cbiAgICAgKi9cbiAgICBjaGlsZHJlbjogUHJvcFR5cGVzLm5vZGUsXG4gICAgLyoqXG4gICAgICogQ29udGVudCBvZiB0aGUgcG9wdXAgaW5mby5cbiAgICAgKi9cbiAgICBjb250ZW50OiBQcm9wVHlwZXMubm9kZSxcbiAgICAvKipcbiAgICAgKiBJcyB0aGUgcG9wdXAgY3VycmVudGx5IGFjdGl2ZS5cbiAgICAgKi9cbiAgICBhY3RpdmU6IFByb3BUeXBlcy5ib29sLFxuICAgIC8qKlxuICAgICAqIFNob3cgcG9wdXAgb24gaG92ZXIgb3IgY2xpY2suXG4gICAgICovXG4gICAgbW9kZTogUHJvcFR5cGVzLm9uZU9mKFsnaG92ZXInLCAnY2xpY2snXSksXG4gICAgLyoqXG4gICAgICogQ1NTIGZvciB0aGUgd3JhcHBlci5cbiAgICAgKi9cbiAgICBjbGFzc19uYW1lOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIFN0eWxlIG9mIHRoZSB3cmFwcGVyLlxuICAgICAqL1xuICAgIHN0eWxlOiBQcm9wVHlwZXMub2JqZWN0LFxuICAgIC8qKlxuICAgICAqIFN0eWxlIGZvciB0aGUgcG9wdXAuXG4gICAgICovXG4gICAgY29udGVudF9zdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICAvKipcbiAgICAgKiBTdHlsZSBmb3IgdGhlIHdyYXBwZWQgY2hpbGRyZW4uXG4gICAgICovXG4gICAgY2hpbGRyZW5fc3R5bGU6IFByb3BUeXBlcy5vYmplY3QsXG5cbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuLyoqXG4gKiBTaW1wbGUgaHRtbC9jc3Mgc3Bpbm5lci5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgU3Bpbm5lciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7Y2xhc3NfbmFtZSwgc3R5bGUsIGlkZW50aXR5fSA9IHRoaXMucHJvcHM7XG4gICAgICAgIHJldHVybiA8ZGl2IGlkPXtpZGVudGl0eX0gY2xhc3NOYW1lPXtjbGFzc19uYW1lfSBzdHlsZT17c3R5bGV9IC8+O1xuICAgIH1cbn1cblxuU3Bpbm5lci5kZWZhdWx0UHJvcHMgPSB7fTtcblxuU3Bpbm5lci5wcm9wVHlwZXMgPSB7XG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICAvKipcbiAgICAgKiAgVW5pcXVlIGlkIGZvciB0aGlzIGNvbXBvbmVudFxuICAgICAqL1xuICAgIGlkZW50aXR5OiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgLyoqXG4gICAgICogVXBkYXRlIGFzcGVjdHMgb24gdGhlIGJhY2tlbmQuXG4gICAgICovXG4gICAgdXBkYXRlQXNwZWN0czogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge21lcmdlQWxsfSBmcm9tICdyYW1kYSc7XG5cbi8qKlxuICogQSBzaG9ydGhhbmQgY29tcG9uZW50IGZvciBhIHN0aWNreSBkaXYuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFN0aWNreSBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICAgICAgaWRlbnRpdHksXG4gICAgICAgICAgICBzdHlsZSxcbiAgICAgICAgICAgIGNoaWxkcmVuLFxuICAgICAgICAgICAgdG9wLFxuICAgICAgICAgICAgbGVmdCxcbiAgICAgICAgICAgIHJpZ2h0LFxuICAgICAgICAgICAgYm90dG9tLFxuICAgICAgICB9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgY29uc3Qgc3R5bGVzID0gbWVyZ2VBbGwoW3N0eWxlLCB7dG9wLCBsZWZ0LCByaWdodCwgYm90dG9tfV0pO1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IGlkPXtpZGVudGl0eX0gc3R5bGU9e3N0eWxlc30+XG4gICAgICAgICAgICAgICAge2NoaWxkcmVufVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5TdGlja3kuZGVmYXVsdFByb3BzID0ge307XG5cbi8vIFRPRE8gQWRkIFN0aWNreSBwcm9wcyBkZXNjcmlwdGlvbnNcblxuU3RpY2t5LnByb3BUeXBlcyA9IHtcbiAgICBjaGlsZHJlbjogUHJvcFR5cGVzLm5vZGUsXG4gICAgdG9wOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIGxlZnQ6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgcmlnaHQ6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgYm90dG9tOiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcbn07XG4iLCJpbXBvcnQgJy4uL3Njc3MvaW5kZXguc2Nzcyc7XG5cbmltcG9ydCBOb3RpY2UgZnJvbSAnLi9jb21wb25lbnRzL05vdGljZSc7XG5pbXBvcnQgUGFnZXIgZnJvbSAnLi9jb21wb25lbnRzL1BhZ2VyJztcbmltcG9ydCBTcGlubmVyIGZyb20gJy4vY29tcG9uZW50cy9TcGlubmVyJztcbmltcG9ydCBTdGlja3kgZnJvbSAnLi9jb21wb25lbnRzL1N0aWNreSc7XG5pbXBvcnQgRHJhd2VyIGZyb20gJy4vY29tcG9uZW50cy9EcmF3ZXInO1xuaW1wb3J0IFBvcFVwIGZyb20gJy4vY29tcG9uZW50cy9Qb3BVcCc7XG5cbmV4cG9ydCB7Tm90aWNlLCBQYWdlciwgU3Bpbm5lciwgU3RpY2t5LCBEcmF3ZXIsIFBvcFVwfTtcbiIsIlxudmFyIGNvbnRlbnQgPSByZXF1aXJlKFwiISEuLi8uLi8uLi9ub2RlX21vZHVsZXMvbWluaS1jc3MtZXh0cmFjdC1wbHVnaW4vZGlzdC9sb2FkZXIuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL2Nzcy1sb2FkZXIvZGlzdC9janMuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL3Nhc3MtbG9hZGVyL2xpYi9sb2FkZXIuanMhLi9pbmRleC5zY3NzXCIpO1xuXG5pZih0eXBlb2YgY29udGVudCA9PT0gJ3N0cmluZycpIGNvbnRlbnQgPSBbW21vZHVsZS5pZCwgY29udGVudCwgJyddXTtcblxudmFyIHRyYW5zZm9ybTtcbnZhciBpbnNlcnRJbnRvO1xuXG5cblxudmFyIG9wdGlvbnMgPSB7XCJobXJcIjp0cnVlfVxuXG5vcHRpb25zLnRyYW5zZm9ybSA9IHRyYW5zZm9ybVxub3B0aW9ucy5pbnNlcnRJbnRvID0gdW5kZWZpbmVkO1xuXG52YXIgdXBkYXRlID0gcmVxdWlyZShcIiEuLi8uLi8uLi9ub2RlX21vZHVsZXMvc3R5bGUtbG9hZGVyL2xpYi9hZGRTdHlsZXMuanNcIikoY29udGVudCwgb3B0aW9ucyk7XG5cbmlmKGNvbnRlbnQubG9jYWxzKSBtb2R1bGUuZXhwb3J0cyA9IGNvbnRlbnQubG9jYWxzO1xuXG5pZihtb2R1bGUuaG90KSB7XG5cdG1vZHVsZS5ob3QuYWNjZXB0KFwiISEuLi8uLi8uLi9ub2RlX21vZHVsZXMvbWluaS1jc3MtZXh0cmFjdC1wbHVnaW4vZGlzdC9sb2FkZXIuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL2Nzcy1sb2FkZXIvZGlzdC9janMuanMhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL3Nhc3MtbG9hZGVyL2xpYi9sb2FkZXIuanMhLi9pbmRleC5zY3NzXCIsIGZ1bmN0aW9uKCkge1xuXHRcdHZhciBuZXdDb250ZW50ID0gcmVxdWlyZShcIiEhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL21pbmktY3NzLWV4dHJhY3QtcGx1Z2luL2Rpc3QvbG9hZGVyLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9jc3MtbG9hZGVyL2Rpc3QvY2pzLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9zYXNzLWxvYWRlci9saWIvbG9hZGVyLmpzIS4vaW5kZXguc2Nzc1wiKTtcblxuXHRcdGlmKHR5cGVvZiBuZXdDb250ZW50ID09PSAnc3RyaW5nJykgbmV3Q29udGVudCA9IFtbbW9kdWxlLmlkLCBuZXdDb250ZW50LCAnJ11dO1xuXG5cdFx0dmFyIGxvY2FscyA9IChmdW5jdGlvbihhLCBiKSB7XG5cdFx0XHR2YXIga2V5LCBpZHggPSAwO1xuXG5cdFx0XHRmb3Ioa2V5IGluIGEpIHtcblx0XHRcdFx0aWYoIWIgfHwgYVtrZXldICE9PSBiW2tleV0pIHJldHVybiBmYWxzZTtcblx0XHRcdFx0aWR4Kys7XG5cdFx0XHR9XG5cblx0XHRcdGZvcihrZXkgaW4gYikgaWR4LS07XG5cblx0XHRcdHJldHVybiBpZHggPT09IDA7XG5cdFx0fShjb250ZW50LmxvY2FscywgbmV3Q29udGVudC5sb2NhbHMpKTtcblxuXHRcdGlmKCFsb2NhbHMpIHRocm93IG5ldyBFcnJvcignQWJvcnRpbmcgQ1NTIEhNUiBkdWUgdG8gY2hhbmdlZCBjc3MtbW9kdWxlcyBsb2NhbHMuJyk7XG5cblx0XHR1cGRhdGUobmV3Q29udGVudCk7XG5cdH0pO1xuXG5cdG1vZHVsZS5ob3QuZGlzcG9zZShmdW5jdGlvbigpIHsgdXBkYXRlKCk7IH0pO1xufSIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyJdLCJzb3VyY2VSb290IjoiIn0=
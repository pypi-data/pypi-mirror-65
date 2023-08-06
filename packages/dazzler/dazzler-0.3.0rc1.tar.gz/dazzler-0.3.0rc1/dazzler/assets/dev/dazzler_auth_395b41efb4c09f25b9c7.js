(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_auth"] = factory(require("react"));
	else
		root["dazzler_auth"] = factory(root["React"]);
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
/******/ 		"auth": 0
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
/******/ 	deferredModules.push([7,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/auth/scss/index.scss":
/*!***********************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/auth/scss/index.scss ***!
  \***********************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./src/auth/js/components/Login.jsx":
/*!******************************************!*\
  !*** ./src/auth/js/components/Login.jsx ***!
  \******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Login; });
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

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }





/**
 * A login form to include on dazzler pages.
 *
 * :CSS:
 *
 *     ``dazzler-auth-login``
 *     - ``login-field``
 *     - ``login-label``
 *     - ``login-input``
 *     - ``login-username``
 *     - ``login-password``
 *     - ``login-button``
 *
 */

var Login =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Login, _React$Component);

  function Login() {
    _classCallCheck(this, Login);

    return _possibleConstructorReturn(this, _getPrototypeOf(Login).apply(this, arguments));
  }

  _createClass(Login, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          class_name = _this$props.class_name,
          style = _this$props.style,
          identity = _this$props.identity,
          method = _this$props.method,
          login_url = _this$props.login_url,
          next_url = _this$props.next_url,
          placeholder_labels = _this$props.placeholder_labels,
          username_label = _this$props.username_label,
          password_label = _this$props.password_label,
          submit_label = _this$props.submit_label,
          footer = _this$props.footer,
          header = _this$props.header;
      var css = Object(commons__WEBPACK_IMPORTED_MODULE_2__["collectTruePropKeys"])(this.props, ['horizontal', 'bordered']);
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("form", {
        className: Object(ramda__WEBPACK_IMPORTED_MODULE_3__["join"])(' ', Object(ramda__WEBPACK_IMPORTED_MODULE_3__["concat"])([class_name], css)),
        style: style,
        id: identity,
        method: method,
        action: login_url
      }, header && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "login-header"
      }, header), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("input", {
        type: "hidden",
        name: "next_url",
        value: next_url || window.location.href
      }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "login-field"
      }, !placeholder_labels && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("label", {
        htmlFor: "login-username-".concat(identity),
        className: "login-label"
      }, username_label), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("input", {
        type: "text",
        name: "username",
        className: "login-field login-username",
        id: "login-username-".concat(identity),
        placeholder: placeholder_labels && username_label
      })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "login-field"
      }, !placeholder_labels && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("label", {
        htmlFor: "login-password-".concat(identity),
        className: "login-label"
      }, password_label), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("input", {
        type: "password",
        name: "password",
        className: "login-field login-password",
        id: "login-password-".concat(identity),
        placeholder: placeholder_labels && password_label
      })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("button", {
        type: "submit",
        className: "login-button"
      }, submit_label), footer && react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "login-footer"
      }, footer));
    }
  }]);

  return Login;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Login.defaultProps = {
  method: 'POST',
  submit_label: 'Login',
  username_label: 'Username',
  password_label: 'Password'
};
Login.propTypes = {
  /**
   * The url to perform login.
   */
  login_url: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,

  /**
   * Redirect to this page after login.
   */
  next_url: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Method to submit the login form.
   */
  method: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * The label to show before the.
   */
  username_label: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Label to replace the password.
   */
  password_label: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Label for the submit button.
   */
  submit_label: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Style the form with the fields side by side.
   */
  horizontal: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,

  /**
   * Apply a border around the
   */
  bordered: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,

  /**
   * Put the label in placeholder attribute instead of a `<label>` element.
   */
  placeholder_labels: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,

  /**
   * Included as first child of the form.
   * Wrapped under div with CSS class ``login-header``
   */
  header: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,

  /**
   * Included at bottom of the login form.
   * Wrapped under div with CSS class ``login-footer``
   */
  footer: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,

  /**
   * Form errors
   */
  errors: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/auth/js/components/Logout.jsx":
/*!*******************************************!*\
  !*** ./src/auth/js/components/Logout.jsx ***!
  \*******************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Logout; });
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
 * A logout button.
 *
 * :CSS:
 *
 *     ``dazzler-auth-logout``
 *     - ``logout-button``
 */

var Logout =
/*#__PURE__*/
function (_React$Component) {
  _inherits(Logout, _React$Component);

  function Logout() {
    _classCallCheck(this, Logout);

    return _possibleConstructorReturn(this, _getPrototypeOf(Logout).apply(this, arguments));
  }

  _createClass(Logout, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          logout_url = _this$props.logout_url,
          label = _this$props.label,
          method = _this$props.method,
          class_name = _this$props.class_name,
          style = _this$props.style,
          identity = _this$props.identity,
          next_url = _this$props.next_url;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("form", {
        action: logout_url,
        method: method,
        className: class_name,
        style: style,
        id: identity
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("input", {
        type: "hidden",
        name: "next_url",
        value: next_url || window.location.href
      }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("button", {
        type: "submit",
        className: "logout-button"
      }, label));
    }
  }]);

  return Logout;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


Logout.defaultProps = {
  method: 'POST',
  label: 'Logout'
};
Logout.propTypes = {
  /**
   * Logout url
   */
  logout_url: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,

  /**
   * Redirect to this page after logout.
   */
  next_url: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Label of the logout button.
   */
  label: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Method to submit the logout form.
   */
  method: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  class_name: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  style: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/auth/js/index.js":
/*!******************************!*\
  !*** ./src/auth/js/index.js ***!
  \******************************/
/*! exports provided: Login, Logout */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _scss_index_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../scss/index.scss */ "./src/auth/scss/index.scss");
/* harmony import */ var _scss_index_scss__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_scss_index_scss__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_Login__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/Login */ "./src/auth/js/components/Login.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Login", function() { return _components_Login__WEBPACK_IMPORTED_MODULE_1__["default"]; });

/* harmony import */ var _components_Logout__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/Logout */ "./src/auth/js/components/Logout.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "Logout", function() { return _components_Logout__WEBPACK_IMPORTED_MODULE_2__["default"]; });






/***/ }),

/***/ "./src/auth/scss/index.scss":
/*!**********************************!*\
  !*** ./src/auth/scss/index.scss ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../../../node_modules/mini-css-extract-plugin/dist/loader.js!../../../node_modules/css-loader/dist/cjs.js!../../../node_modules/sass-loader/lib/loader.js!./index.scss */ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/sass-loader/lib/loader.js!./src/auth/scss/index.scss");

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

/***/ 7:
/*!************************************!*\
  !*** multi ./src/auth/js/index.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/auth/js/index.js */"./src/auth/js/index.js");


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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8uL3NyYy9hdXRoL3Njc3MvaW5kZXguc2Nzcz8uL25vZGVfbW9kdWxlcy9taW5pLWNzcy1leHRyYWN0LXBsdWdpbi9kaXN0L2xvYWRlci5qcyEuL25vZGVfbW9kdWxlcy9jc3MtbG9hZGVyL2Rpc3QvY2pzLmpzIS4vbm9kZV9tb2R1bGVzL3Nhc3MtbG9hZGVyL2xpYi9sb2FkZXIuanMiLCJ3ZWJwYWNrOi8vLy4vc3JjL2F1dGgvanMvY29tcG9uZW50cy9Mb2dpbi5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9hdXRoL2pzL2NvbXBvbmVudHMvTG9nb3V0LmpzeD8iLCJ3ZWJwYWNrOi8vLy4vc3JjL2F1dGgvanMvaW5kZXguanM/Iiwid2VicGFjazovLy8uL3NyYy9hdXRoL3Njc3MvaW5kZXguc2Nzcz8iLCJ3ZWJwYWNrOi8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Il0sIm5hbWVzIjpbIkxvZ2luIiwicHJvcHMiLCJjbGFzc19uYW1lIiwic3R5bGUiLCJpZGVudGl0eSIsIm1ldGhvZCIsImxvZ2luX3VybCIsIm5leHRfdXJsIiwicGxhY2Vob2xkZXJfbGFiZWxzIiwidXNlcm5hbWVfbGFiZWwiLCJwYXNzd29yZF9sYWJlbCIsInN1Ym1pdF9sYWJlbCIsImZvb3RlciIsImhlYWRlciIsImNzcyIsImNvbGxlY3RUcnVlUHJvcEtleXMiLCJqb2luIiwiY29uY2F0Iiwid2luZG93IiwibG9jYXRpb24iLCJocmVmIiwiUmVhY3QiLCJDb21wb25lbnQiLCJkZWZhdWx0UHJvcHMiLCJwcm9wVHlwZXMiLCJQcm9wVHlwZXMiLCJzdHJpbmciLCJpc1JlcXVpcmVkIiwiaG9yaXpvbnRhbCIsImJvb2wiLCJib3JkZXJlZCIsIm5vZGUiLCJlcnJvcnMiLCJvYmplY3QiLCJ1cGRhdGVBc3BlY3RzIiwiZnVuYyIsIkxvZ291dCIsImxvZ291dF91cmwiLCJsYWJlbCJdLCJtYXBwaW5ncyI6IkFBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQztBQUNELE87QUNWQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGdCQUFRLG9CQUFvQjtBQUM1QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHlCQUFpQiw0QkFBNEI7QUFDN0M7QUFDQTtBQUNBLDBCQUFrQiwyQkFBMkI7QUFDN0M7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7O0FBR0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGtEQUEwQyxnQ0FBZ0M7QUFDMUU7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxnRUFBd0Qsa0JBQWtCO0FBQzFFO0FBQ0EseURBQWlELGNBQWM7QUFDL0Q7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlEQUF5QyxpQ0FBaUM7QUFDMUUsd0hBQWdILG1CQUFtQixFQUFFO0FBQ3JJO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsbUNBQTJCLDBCQUEwQixFQUFF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QUFTLENBQUNDLE1BdkJMO0FBd0JmUSxlQUFhLEVBQUVULGlEQUFTLENBQUNVO0FBeEJWLENBQW5CLEM7Ozs7Ozs7Ozs7OztBQ2hEQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUVBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7QUNGQSxjQUFjLG1CQUFPLENBQUMsZ1ZBQTBLOztBQUVoTSw0Q0FBNEMsUUFBUzs7QUFFckQ7QUFDQTs7OztBQUlBLGVBQWU7O0FBRWY7QUFDQTs7QUFFQSxhQUFhLG1CQUFPLENBQUMseUdBQXNEOztBQUUzRTs7QUFFQSxHQUFHLEtBQVUsRUFBRSxFOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ25CZixtRCIsImZpbGUiOiJkYXp6bGVyX2F1dGhfMzk1YjQxZWZiNGMwOWYyNWI5YzcuanMiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2F1dGhcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9hdXRoXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0pO1xufSkod2luZG93LCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCIgXHQvLyBpbnN0YWxsIGEgSlNPTlAgY2FsbGJhY2sgZm9yIGNodW5rIGxvYWRpbmdcbiBcdGZ1bmN0aW9uIHdlYnBhY2tKc29ucENhbGxiYWNrKGRhdGEpIHtcbiBcdFx0dmFyIGNodW5rSWRzID0gZGF0YVswXTtcbiBcdFx0dmFyIG1vcmVNb2R1bGVzID0gZGF0YVsxXTtcbiBcdFx0dmFyIGV4ZWN1dGVNb2R1bGVzID0gZGF0YVsyXTtcblxuIFx0XHQvLyBhZGQgXCJtb3JlTW9kdWxlc1wiIHRvIHRoZSBtb2R1bGVzIG9iamVjdCxcbiBcdFx0Ly8gdGhlbiBmbGFnIGFsbCBcImNodW5rSWRzXCIgYXMgbG9hZGVkIGFuZCBmaXJlIGNhbGxiYWNrXG4gXHRcdHZhciBtb2R1bGVJZCwgY2h1bmtJZCwgaSA9IDAsIHJlc29sdmVzID0gW107XG4gXHRcdGZvcig7aSA8IGNodW5rSWRzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0Y2h1bmtJZCA9IGNodW5rSWRzW2ldO1xuIFx0XHRcdGlmKGluc3RhbGxlZENodW5rc1tjaHVua0lkXSkge1xuIFx0XHRcdFx0cmVzb2x2ZXMucHVzaChpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF1bMF0pO1xuIFx0XHRcdH1cbiBcdFx0XHRpbnN0YWxsZWRDaHVua3NbY2h1bmtJZF0gPSAwO1xuIFx0XHR9XG4gXHRcdGZvcihtb2R1bGVJZCBpbiBtb3JlTW9kdWxlcykge1xuIFx0XHRcdGlmKE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChtb3JlTW9kdWxlcywgbW9kdWxlSWQpKSB7XG4gXHRcdFx0XHRtb2R1bGVzW21vZHVsZUlkXSA9IG1vcmVNb2R1bGVzW21vZHVsZUlkXTtcbiBcdFx0XHR9XG4gXHRcdH1cbiBcdFx0aWYocGFyZW50SnNvbnBGdW5jdGlvbikgcGFyZW50SnNvbnBGdW5jdGlvbihkYXRhKTtcblxuIFx0XHR3aGlsZShyZXNvbHZlcy5sZW5ndGgpIHtcbiBcdFx0XHRyZXNvbHZlcy5zaGlmdCgpKCk7XG4gXHRcdH1cblxuIFx0XHQvLyBhZGQgZW50cnkgbW9kdWxlcyBmcm9tIGxvYWRlZCBjaHVuayB0byBkZWZlcnJlZCBsaXN0XG4gXHRcdGRlZmVycmVkTW9kdWxlcy5wdXNoLmFwcGx5KGRlZmVycmVkTW9kdWxlcywgZXhlY3V0ZU1vZHVsZXMgfHwgW10pO1xuXG4gXHRcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gYWxsIGNodW5rcyByZWFkeVxuIFx0XHRyZXR1cm4gY2hlY2tEZWZlcnJlZE1vZHVsZXMoKTtcbiBcdH07XG4gXHRmdW5jdGlvbiBjaGVja0RlZmVycmVkTW9kdWxlcygpIHtcbiBcdFx0dmFyIHJlc3VsdDtcbiBcdFx0Zm9yKHZhciBpID0gMDsgaSA8IGRlZmVycmVkTW9kdWxlcy5sZW5ndGg7IGkrKykge1xuIFx0XHRcdHZhciBkZWZlcnJlZE1vZHVsZSA9IGRlZmVycmVkTW9kdWxlc1tpXTtcbiBcdFx0XHR2YXIgZnVsZmlsbGVkID0gdHJ1ZTtcbiBcdFx0XHRmb3IodmFyIGogPSAxOyBqIDwgZGVmZXJyZWRNb2R1bGUubGVuZ3RoOyBqKyspIHtcbiBcdFx0XHRcdHZhciBkZXBJZCA9IGRlZmVycmVkTW9kdWxlW2pdO1xuIFx0XHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2RlcElkXSAhPT0gMCkgZnVsZmlsbGVkID0gZmFsc2U7XG4gXHRcdFx0fVxuIFx0XHRcdGlmKGZ1bGZpbGxlZCkge1xuIFx0XHRcdFx0ZGVmZXJyZWRNb2R1bGVzLnNwbGljZShpLS0sIDEpO1xuIFx0XHRcdFx0cmVzdWx0ID0gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSBkZWZlcnJlZE1vZHVsZVswXSk7XG4gXHRcdFx0fVxuIFx0XHR9XG5cbiBcdFx0cmV0dXJuIHJlc3VsdDtcbiBcdH1cblxuIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gb2JqZWN0IHRvIHN0b3JlIGxvYWRlZCBhbmQgbG9hZGluZyBjaHVua3NcbiBcdC8vIHVuZGVmaW5lZCA9IGNodW5rIG5vdCBsb2FkZWQsIG51bGwgPSBjaHVuayBwcmVsb2FkZWQvcHJlZmV0Y2hlZFxuIFx0Ly8gUHJvbWlzZSA9IGNodW5rIGxvYWRpbmcsIDAgPSBjaHVuayBsb2FkZWRcbiBcdHZhciBpbnN0YWxsZWRDaHVua3MgPSB7XG4gXHRcdFwiYXV0aFwiOiAwXG4gXHR9O1xuXG4gXHR2YXIgZGVmZXJyZWRNb2R1bGVzID0gW107XG5cbiBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4gXHRmdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cbiBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4gXHRcdGlmKGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdKSB7XG4gXHRcdFx0cmV0dXJuIGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdLmV4cG9ydHM7XG4gXHRcdH1cbiBcdFx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcbiBcdFx0dmFyIG1vZHVsZSA9IGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdID0ge1xuIFx0XHRcdGk6IG1vZHVsZUlkLFxuIFx0XHRcdGw6IGZhbHNlLFxuIFx0XHRcdGV4cG9ydHM6IHt9XG4gXHRcdH07XG5cbiBcdFx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG4gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG4gXHRcdC8vIEZsYWcgdGhlIG1vZHVsZSBhcyBsb2FkZWRcbiBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuXG4gXHRcdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG4gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbiBcdH1cblxuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZXMgb2JqZWN0IChfX3dlYnBhY2tfbW9kdWxlc19fKVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5tID0gbW9kdWxlcztcblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGUgY2FjaGVcbiBcdF9fd2VicGFja19yZXF1aXJlX18uYyA9IGluc3RhbGxlZE1vZHVsZXM7XG5cbiBcdC8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb24gZm9yIGhhcm1vbnkgZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4gXHRcdGlmKCFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywgbmFtZSkpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgbmFtZSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGdldHRlciB9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZGVmaW5lIF9fZXNNb2R1bGUgb24gZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yID0gZnVuY3Rpb24oZXhwb3J0cykge1xuIFx0XHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcbiBcdFx0fVxuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xuIFx0fTtcblxuIFx0Ly8gY3JlYXRlIGEgZmFrZSBuYW1lc3BhY2Ugb2JqZWN0XG4gXHQvLyBtb2RlICYgMTogdmFsdWUgaXMgYSBtb2R1bGUgaWQsIHJlcXVpcmUgaXRcbiBcdC8vIG1vZGUgJiAyOiBtZXJnZSBhbGwgcHJvcGVydGllcyBvZiB2YWx1ZSBpbnRvIHRoZSBuc1xuIFx0Ly8gbW9kZSAmIDQ6IHJldHVybiB2YWx1ZSB3aGVuIGFscmVhZHkgbnMgb2JqZWN0XG4gXHQvLyBtb2RlICYgOHwxOiBiZWhhdmUgbGlrZSByZXF1aXJlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnQgPSBmdW5jdGlvbih2YWx1ZSwgbW9kZSkge1xuIFx0XHRpZihtb2RlICYgMSkgdmFsdWUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKHZhbHVlKTtcbiBcdFx0aWYobW9kZSAmIDgpIHJldHVybiB2YWx1ZTtcbiBcdFx0aWYoKG1vZGUgJiA0KSAmJiB0eXBlb2YgdmFsdWUgPT09ICdvYmplY3QnICYmIHZhbHVlICYmIHZhbHVlLl9fZXNNb2R1bGUpIHJldHVybiB2YWx1ZTtcbiBcdFx0dmFyIG5zID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yKG5zKTtcbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KG5zLCAnZGVmYXVsdCcsIHsgZW51bWVyYWJsZTogdHJ1ZSwgdmFsdWU6IHZhbHVlIH0pO1xuIFx0XHRpZihtb2RlICYgMiAmJiB0eXBlb2YgdmFsdWUgIT0gJ3N0cmluZycpIGZvcih2YXIga2V5IGluIHZhbHVlKSBfX3dlYnBhY2tfcmVxdWlyZV9fLmQobnMsIGtleSwgZnVuY3Rpb24oa2V5KSB7IHJldHVybiB2YWx1ZVtrZXldOyB9LmJpbmQobnVsbCwga2V5KSk7XG4gXHRcdHJldHVybiBucztcbiBcdH07XG5cbiBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm4gPSBmdW5jdGlvbihtb2R1bGUpIHtcbiBcdFx0dmFyIGdldHRlciA9IG1vZHVsZSAmJiBtb2R1bGUuX19lc01vZHVsZSA/XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbiBcdFx0XHRmdW5jdGlvbiBnZXRNb2R1bGVFeHBvcnRzKCkgeyByZXR1cm4gbW9kdWxlOyB9O1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQoZ2V0dGVyLCAnYScsIGdldHRlcik7XG4gXHRcdHJldHVybiBnZXR0ZXI7XG4gXHR9O1xuXG4gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubyA9IGZ1bmN0aW9uKG9iamVjdCwgcHJvcGVydHkpIHsgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsIHByb3BlcnR5KTsgfTtcblxuIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbiBcdF9fd2VicGFja19yZXF1aXJlX18ucCA9IFwiXCI7XG5cbiBcdHZhciBqc29ucEFycmF5ID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSA9IHdpbmRvd1tcIndlYnBhY2tKc29ucGRhenpsZXJfbmFtZV9cIl0gfHwgW107XG4gXHR2YXIgb2xkSnNvbnBGdW5jdGlvbiA9IGpzb25wQXJyYXkucHVzaC5iaW5kKGpzb25wQXJyYXkpO1xuIFx0anNvbnBBcnJheS5wdXNoID0gd2VicGFja0pzb25wQ2FsbGJhY2s7XG4gXHRqc29ucEFycmF5ID0ganNvbnBBcnJheS5zbGljZSgpO1xuIFx0Zm9yKHZhciBpID0gMDsgaSA8IGpzb25wQXJyYXkubGVuZ3RoOyBpKyspIHdlYnBhY2tKc29ucENhbGxiYWNrKGpzb25wQXJyYXlbaV0pO1xuIFx0dmFyIHBhcmVudEpzb25wRnVuY3Rpb24gPSBvbGRKc29ucEZ1bmN0aW9uO1xuXG5cbiBcdC8vIGFkZCBlbnRyeSBtb2R1bGUgdG8gZGVmZXJyZWQgbGlzdFxuIFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2goWzcsXCJjb21tb25zXCJdKTtcbiBcdC8vIHJ1biBkZWZlcnJlZCBtb2R1bGVzIHdoZW4gcmVhZHlcbiBcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIiwiLy8gZXh0cmFjdGVkIGJ5IG1pbmktY3NzLWV4dHJhY3QtcGx1Z2luIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQge2NvbGxlY3RUcnVlUHJvcEtleXN9IGZyb20gJ2NvbW1vbnMnO1xuaW1wb3J0IHtjb25jYXQsIGpvaW59IGZyb20gJ3JhbWRhJztcblxuLyoqXG4gKiBBIGxvZ2luIGZvcm0gdG8gaW5jbHVkZSBvbiBkYXp6bGVyIHBhZ2VzLlxuICpcbiAqIDpDU1M6XG4gKlxuICogICAgIGBgZGF6emxlci1hdXRoLWxvZ2luYGBcbiAqICAgICAtIGBgbG9naW4tZmllbGRgYFxuICogICAgIC0gYGBsb2dpbi1sYWJlbGBgXG4gKiAgICAgLSBgYGxvZ2luLWlucHV0YGBcbiAqICAgICAtIGBgbG9naW4tdXNlcm5hbWVgYFxuICogICAgIC0gYGBsb2dpbi1wYXNzd29yZGBgXG4gKiAgICAgLSBgYGxvZ2luLWJ1dHRvbmBgXG4gKlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBMb2dpbiBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICAgICAgc3R5bGUsXG4gICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgIG1ldGhvZCxcbiAgICAgICAgICAgIGxvZ2luX3VybCxcbiAgICAgICAgICAgIG5leHRfdXJsLFxuICAgICAgICAgICAgcGxhY2Vob2xkZXJfbGFiZWxzLFxuICAgICAgICAgICAgdXNlcm5hbWVfbGFiZWwsXG4gICAgICAgICAgICBwYXNzd29yZF9sYWJlbCxcbiAgICAgICAgICAgIHN1Ym1pdF9sYWJlbCxcbiAgICAgICAgICAgIGZvb3RlcixcbiAgICAgICAgICAgIGhlYWRlcixcbiAgICAgICAgfSA9IHRoaXMucHJvcHM7XG5cbiAgICAgICAgY29uc3QgY3NzID0gY29sbGVjdFRydWVQcm9wS2V5cyh0aGlzLnByb3BzLCBbJ2hvcml6b250YWwnLCAnYm9yZGVyZWQnXSk7XG5cbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxmb3JtXG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lPXtqb2luKCcgJywgY29uY2F0KFtjbGFzc19uYW1lXSwgY3NzKSl9XG4gICAgICAgICAgICAgICAgc3R5bGU9e3N0eWxlfVxuICAgICAgICAgICAgICAgIGlkPXtpZGVudGl0eX1cbiAgICAgICAgICAgICAgICBtZXRob2Q9e21ldGhvZH1cbiAgICAgICAgICAgICAgICBhY3Rpb249e2xvZ2luX3VybH1cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICB7aGVhZGVyICYmIDxkaXYgY2xhc3NOYW1lPVwibG9naW4taGVhZGVyXCI+e2hlYWRlcn08L2Rpdj59XG4gICAgICAgICAgICAgICAgPGlucHV0XG4gICAgICAgICAgICAgICAgICAgIHR5cGU9XCJoaWRkZW5cIlxuICAgICAgICAgICAgICAgICAgICBuYW1lPVwibmV4dF91cmxcIlxuICAgICAgICAgICAgICAgICAgICB2YWx1ZT17bmV4dF91cmwgfHwgd2luZG93LmxvY2F0aW9uLmhyZWZ9XG4gICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImxvZ2luLWZpZWxkXCI+XG4gICAgICAgICAgICAgICAgICAgIHshcGxhY2Vob2xkZXJfbGFiZWxzICYmIChcbiAgICAgICAgICAgICAgICAgICAgICAgIDxsYWJlbFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGh0bWxGb3I9e2Bsb2dpbi11c2VybmFtZS0ke2lkZW50aXR5fWB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwibG9naW4tbGFiZWxcIlxuICAgICAgICAgICAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt1c2VybmFtZV9sYWJlbH1cbiAgICAgICAgICAgICAgICAgICAgICAgIDwvbGFiZWw+XG4gICAgICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICAgICAgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT1cInVzZXJuYW1lXCJcbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImxvZ2luLWZpZWxkIGxvZ2luLXVzZXJuYW1lXCJcbiAgICAgICAgICAgICAgICAgICAgICAgIGlkPXtgbG9naW4tdXNlcm5hbWUtJHtpZGVudGl0eX1gfVxuICAgICAgICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9e3BsYWNlaG9sZGVyX2xhYmVscyAmJiB1c2VybmFtZV9sYWJlbH1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImxvZ2luLWZpZWxkXCI+XG4gICAgICAgICAgICAgICAgICAgIHshcGxhY2Vob2xkZXJfbGFiZWxzICYmIChcbiAgICAgICAgICAgICAgICAgICAgICAgIDxsYWJlbFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGh0bWxGb3I9e2Bsb2dpbi1wYXNzd29yZC0ke2lkZW50aXR5fWB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwibG9naW4tbGFiZWxcIlxuICAgICAgICAgICAgICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtwYXNzd29yZF9sYWJlbH1cbiAgICAgICAgICAgICAgICAgICAgICAgIDwvbGFiZWw+XG4gICAgICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICAgICAgdHlwZT1cInBhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9XCJwYXNzd29yZFwiXG4gICAgICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJsb2dpbi1maWVsZCBsb2dpbi1wYXNzd29yZFwiXG4gICAgICAgICAgICAgICAgICAgICAgICBpZD17YGxvZ2luLXBhc3N3b3JkLSR7aWRlbnRpdHl9YH1cbiAgICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtwbGFjZWhvbGRlcl9sYWJlbHMgJiYgcGFzc3dvcmRfbGFiZWx9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwic3VibWl0XCIgY2xhc3NOYW1lPVwibG9naW4tYnV0dG9uXCI+XG4gICAgICAgICAgICAgICAgICAgIHtzdWJtaXRfbGFiZWx9XG4gICAgICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgICAgICAge2Zvb3RlciAmJiA8ZGl2IGNsYXNzTmFtZT1cImxvZ2luLWZvb3RlclwiPntmb290ZXJ9PC9kaXY+fVxuICAgICAgICAgICAgPC9mb3JtPlxuICAgICAgICApO1xuICAgIH1cbn1cblxuTG9naW4uZGVmYXVsdFByb3BzID0ge1xuICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgIHN1Ym1pdF9sYWJlbDogJ0xvZ2luJyxcbiAgICB1c2VybmFtZV9sYWJlbDogJ1VzZXJuYW1lJyxcbiAgICBwYXNzd29yZF9sYWJlbDogJ1Bhc3N3b3JkJyxcbn07XG5cbkxvZ2luLnByb3BUeXBlcyA9IHtcbiAgICAvKipcbiAgICAgKiBUaGUgdXJsIHRvIHBlcmZvcm0gbG9naW4uXG4gICAgICovXG4gICAgbG9naW5fdXJsOiBQcm9wVHlwZXMuc3RyaW5nLmlzUmVxdWlyZWQsXG4gICAgLyoqXG4gICAgICogUmVkaXJlY3QgdG8gdGhpcyBwYWdlIGFmdGVyIGxvZ2luLlxuICAgICAqL1xuICAgIG5leHRfdXJsOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIE1ldGhvZCB0byBzdWJtaXQgdGhlIGxvZ2luIGZvcm0uXG4gICAgICovXG4gICAgbWV0aG9kOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIC8qKlxuICAgICAqIFRoZSBsYWJlbCB0byBzaG93IGJlZm9yZSB0aGUuXG4gICAgICovXG4gICAgdXNlcm5hbWVfbGFiZWw6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogTGFiZWwgdG8gcmVwbGFjZSB0aGUgcGFzc3dvcmQuXG4gICAgICovXG4gICAgcGFzc3dvcmRfbGFiZWw6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgLyoqXG4gICAgICogTGFiZWwgZm9yIHRoZSBzdWJtaXQgYnV0dG9uLlxuICAgICAqL1xuICAgIHN1Ym1pdF9sYWJlbDogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAvKipcbiAgICAgKiBTdHlsZSB0aGUgZm9ybSB3aXRoIHRoZSBmaWVsZHMgc2lkZSBieSBzaWRlLlxuICAgICAqL1xuICAgIGhvcml6b250YWw6IFByb3BUeXBlcy5ib29sLFxuICAgIC8qKlxuICAgICAqIEFwcGx5IGEgYm9yZGVyIGFyb3VuZCB0aGVcbiAgICAgKi9cbiAgICBib3JkZXJlZDogUHJvcFR5cGVzLmJvb2wsXG4gICAgLyoqXG4gICAgICogUHV0IHRoZSBsYWJlbCBpbiBwbGFjZWhvbGRlciBhdHRyaWJ1dGUgaW5zdGVhZCBvZiBhIGA8bGFiZWw+YCBlbGVtZW50LlxuICAgICAqL1xuICAgIHBsYWNlaG9sZGVyX2xhYmVsczogUHJvcFR5cGVzLmJvb2wsXG5cbiAgICAvKipcbiAgICAgKiBJbmNsdWRlZCBhcyBmaXJzdCBjaGlsZCBvZiB0aGUgZm9ybS5cbiAgICAgKiBXcmFwcGVkIHVuZGVyIGRpdiB3aXRoIENTUyBjbGFzcyBgYGxvZ2luLWhlYWRlcmBgXG4gICAgICovXG4gICAgaGVhZGVyOiBQcm9wVHlwZXMubm9kZSxcblxuICAgIC8qKlxuICAgICAqIEluY2x1ZGVkIGF0IGJvdHRvbSBvZiB0aGUgbG9naW4gZm9ybS5cbiAgICAgKiBXcmFwcGVkIHVuZGVyIGRpdiB3aXRoIENTUyBjbGFzcyBgYGxvZ2luLWZvb3RlcmBgXG4gICAgICovXG4gICAgZm9vdGVyOiBQcm9wVHlwZXMubm9kZSxcblxuICAgIC8qKlxuICAgICAqIEZvcm0gZXJyb3JzXG4gICAgICovXG4gICAgZXJyb3JzOiBQcm9wVHlwZXMub2JqZWN0LFxuXG4gICAgY2xhc3NfbmFtZTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzdHlsZTogUHJvcFR5cGVzLm9iamVjdCxcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuLyoqXG4gKiBBIGxvZ291dCBidXR0b24uXG4gKlxuICogOkNTUzpcbiAqXG4gKiAgICAgYGBkYXp6bGVyLWF1dGgtbG9nb3V0YGBcbiAqICAgICAtIGBgbG9nb3V0LWJ1dHRvbmBgXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIExvZ291dCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudCB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBsb2dvdXRfdXJsLFxuICAgICAgICAgICAgbGFiZWwsXG4gICAgICAgICAgICBtZXRob2QsXG4gICAgICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICAgICAgc3R5bGUsXG4gICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgIG5leHRfdXJsLFxuICAgICAgICB9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxmb3JtXG4gICAgICAgICAgICAgICAgYWN0aW9uPXtsb2dvdXRfdXJsfVxuICAgICAgICAgICAgICAgIG1ldGhvZD17bWV0aG9kfVxuICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17Y2xhc3NfbmFtZX1cbiAgICAgICAgICAgICAgICBzdHlsZT17c3R5bGV9XG4gICAgICAgICAgICAgICAgaWQ9e2lkZW50aXR5fVxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICB0eXBlPVwiaGlkZGVuXCJcbiAgICAgICAgICAgICAgICAgICAgbmFtZT1cIm5leHRfdXJsXCJcbiAgICAgICAgICAgICAgICAgICAgdmFsdWU9e25leHRfdXJsIHx8IHdpbmRvdy5sb2NhdGlvbi5ocmVmfVxuICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwic3VibWl0XCIgY2xhc3NOYW1lPVwibG9nb3V0LWJ1dHRvblwiPlxuICAgICAgICAgICAgICAgICAgICB7bGFiZWx9XG4gICAgICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgICA8L2Zvcm0+XG4gICAgICAgICk7XG4gICAgfVxufVxuXG5Mb2dvdXQuZGVmYXVsdFByb3BzID0ge1xuICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgIGxhYmVsOiAnTG9nb3V0Jyxcbn07XG5cbkxvZ291dC5wcm9wVHlwZXMgPSB7XG4gICAgLyoqXG4gICAgICogTG9nb3V0IHVybFxuICAgICAqL1xuICAgIGxvZ291dF91cmw6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcblxuICAgIC8qKlxuICAgICAqIFJlZGlyZWN0IHRvIHRoaXMgcGFnZSBhZnRlciBsb2dvdXQuXG4gICAgICovXG4gICAgbmV4dF91cmw6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBMYWJlbCBvZiB0aGUgbG9nb3V0IGJ1dHRvbi5cbiAgICAgKi9cbiAgICBsYWJlbDogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIC8qKlxuICAgICAqIE1ldGhvZCB0byBzdWJtaXQgdGhlIGxvZ291dCBmb3JtLlxuICAgICAqL1xuICAgIG1ldGhvZDogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIGNsYXNzX25hbWU6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgc3R5bGU6IFByb3BUeXBlcy5vYmplY3QsXG4gICAgaWRlbnRpdHk6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgdXBkYXRlQXNwZWN0czogUHJvcFR5cGVzLmZ1bmMsXG59O1xuIiwiaW1wb3J0ICcuLi9zY3NzL2luZGV4LnNjc3MnO1xuXG5pbXBvcnQgTG9naW4gZnJvbSAnLi9jb21wb25lbnRzL0xvZ2luJztcbmltcG9ydCBMb2dvdXQgZnJvbSAnLi9jb21wb25lbnRzL0xvZ291dCc7XG5cbmV4cG9ydCB7TG9naW4sIExvZ291dH07XG4iLCJcbnZhciBjb250ZW50ID0gcmVxdWlyZShcIiEhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL21pbmktY3NzLWV4dHJhY3QtcGx1Z2luL2Rpc3QvbG9hZGVyLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9jc3MtbG9hZGVyL2Rpc3QvY2pzLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9zYXNzLWxvYWRlci9saWIvbG9hZGVyLmpzIS4vaW5kZXguc2Nzc1wiKTtcblxuaWYodHlwZW9mIGNvbnRlbnQgPT09ICdzdHJpbmcnKSBjb250ZW50ID0gW1ttb2R1bGUuaWQsIGNvbnRlbnQsICcnXV07XG5cbnZhciB0cmFuc2Zvcm07XG52YXIgaW5zZXJ0SW50bztcblxuXG5cbnZhciBvcHRpb25zID0ge1wiaG1yXCI6dHJ1ZX1cblxub3B0aW9ucy50cmFuc2Zvcm0gPSB0cmFuc2Zvcm1cbm9wdGlvbnMuaW5zZXJ0SW50byA9IHVuZGVmaW5lZDtcblxudmFyIHVwZGF0ZSA9IHJlcXVpcmUoXCIhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL3N0eWxlLWxvYWRlci9saWIvYWRkU3R5bGVzLmpzXCIpKGNvbnRlbnQsIG9wdGlvbnMpO1xuXG5pZihjb250ZW50LmxvY2FscykgbW9kdWxlLmV4cG9ydHMgPSBjb250ZW50LmxvY2FscztcblxuaWYobW9kdWxlLmhvdCkge1xuXHRtb2R1bGUuaG90LmFjY2VwdChcIiEhLi4vLi4vLi4vbm9kZV9tb2R1bGVzL21pbmktY3NzLWV4dHJhY3QtcGx1Z2luL2Rpc3QvbG9hZGVyLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9jc3MtbG9hZGVyL2Rpc3QvY2pzLmpzIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9zYXNzLWxvYWRlci9saWIvbG9hZGVyLmpzIS4vaW5kZXguc2Nzc1wiLCBmdW5jdGlvbigpIHtcblx0XHR2YXIgbmV3Q29udGVudCA9IHJlcXVpcmUoXCIhIS4uLy4uLy4uL25vZGVfbW9kdWxlcy9taW5pLWNzcy1leHRyYWN0LXBsdWdpbi9kaXN0L2xvYWRlci5qcyEuLi8uLi8uLi9ub2RlX21vZHVsZXMvY3NzLWxvYWRlci9kaXN0L2Nqcy5qcyEuLi8uLi8uLi9ub2RlX21vZHVsZXMvc2Fzcy1sb2FkZXIvbGliL2xvYWRlci5qcyEuL2luZGV4LnNjc3NcIik7XG5cblx0XHRpZih0eXBlb2YgbmV3Q29udGVudCA9PT0gJ3N0cmluZycpIG5ld0NvbnRlbnQgPSBbW21vZHVsZS5pZCwgbmV3Q29udGVudCwgJyddXTtcblxuXHRcdHZhciBsb2NhbHMgPSAoZnVuY3Rpb24oYSwgYikge1xuXHRcdFx0dmFyIGtleSwgaWR4ID0gMDtcblxuXHRcdFx0Zm9yKGtleSBpbiBhKSB7XG5cdFx0XHRcdGlmKCFiIHx8IGFba2V5XSAhPT0gYltrZXldKSByZXR1cm4gZmFsc2U7XG5cdFx0XHRcdGlkeCsrO1xuXHRcdFx0fVxuXG5cdFx0XHRmb3Ioa2V5IGluIGIpIGlkeC0tO1xuXG5cdFx0XHRyZXR1cm4gaWR4ID09PSAwO1xuXHRcdH0oY29udGVudC5sb2NhbHMsIG5ld0NvbnRlbnQubG9jYWxzKSk7XG5cblx0XHRpZighbG9jYWxzKSB0aHJvdyBuZXcgRXJyb3IoJ0Fib3J0aW5nIENTUyBITVIgZHVlIHRvIGNoYW5nZWQgY3NzLW1vZHVsZXMgbG9jYWxzLicpO1xuXG5cdFx0dXBkYXRlKG5ld0NvbnRlbnQpO1xuXHR9KTtcblxuXHRtb2R1bGUuaG90LmRpc3Bvc2UoZnVuY3Rpb24oKSB7IHVwZGF0ZSgpOyB9KTtcbn0iLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiXSwic291cmNlUm9vdCI6IiJ9
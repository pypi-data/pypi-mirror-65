(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_test"] = factory(require("react"));
	else
		root["dazzler_test"] = factory(root["React"]);
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
/******/ 		"test": 0
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
/******/ 	deferredModules.push([2,"commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/internal/test_components/components/ComponentAsAspect.jsx":
/*!***********************************************************************!*\
  !*** ./src/internal/test_components/components/ComponentAsAspect.jsx ***!
  \***********************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return ComponentAsAspect; });
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




var ComponentAsAspect =
/*#__PURE__*/
function (_React$Component) {
  _inherits(ComponentAsAspect, _React$Component);

  function ComponentAsAspect() {
    _classCallCheck(this, ComponentAsAspect);

    return _possibleConstructorReturn(this, _getPrototypeOf(ComponentAsAspect).apply(this, arguments));
  }

  _createClass(ComponentAsAspect, [{
    key: "render",
    value: function render() {
      var _this$props = this.props,
          identity = _this$props.identity,
          single = _this$props.single,
          array = _this$props.array,
          shape = _this$props.shape;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: identity
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "single"
      }, single), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "array"
      }, array.map(function (e, i) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          key: i
        }, e);
      })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "shape"
      }, shape.shaped));
    }
  }]);

  return ComponentAsAspect;
}(react__WEBPACK_IMPORTED_MODULE_0___default.a.Component);


ComponentAsAspect.defaultProps = {};
ComponentAsAspect.propTypes = {
  single: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.element,
  array: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.element),
  shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
    shaped: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.element
  }),

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

/***/ "./src/internal/test_components/components/DefaultProps.jsx":
/*!******************************************************************!*\
  !*** ./src/internal/test_components/components/DefaultProps.jsx ***!
  \******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return DefaultProps; });
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




var DefaultProps =
/*#__PURE__*/
function (_Component) {
  _inherits(DefaultProps, _Component);

  function DefaultProps() {
    _classCallCheck(this, DefaultProps);

    return _possibleConstructorReturn(this, _getPrototypeOf(DefaultProps).apply(this, arguments));
  }

  _createClass(DefaultProps, [{
    key: "render",
    value: function render() {
      var id = this.props.id;
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: id
      }, Object.entries(this.props).map(function (k, v) {
        return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
          id: "".concat(id, "-").concat(k),
          key: "".concat(id, "-").concat(k)
        }, k, ": ", JSON.stringify(v));
      }));
    }
  }]);

  return DefaultProps;
}(react__WEBPACK_IMPORTED_MODULE_0__["Component"]);


DefaultProps.defaultProps = {
  string_default: 'Default string',
  string_default_empty: '',
  number_default: 0.2666,
  number_default_empty: 0,
  array_default: [1, 2, 3],
  array_default_empty: [],
  object_default: {
    foo: 'bar'
  },
  object_default_empty: {}
};
DefaultProps.propTypes = {
  id: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  string_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  string_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  number_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  number_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  array_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  array_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  object_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  object_default_empty: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object
};

/***/ }),

/***/ "./src/internal/test_components/components/TestComponent.jsx":
/*!*******************************************************************!*\
  !*** ./src/internal/test_components/components/TestComponent.jsx ***!
  \*******************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return TestComponent; });
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
 * Test component with all supported props by dazzler.
 * Each prop are rendered with a selector for easy access.
 */

var TestComponent =
/*#__PURE__*/
function (_Component) {
  _inherits(TestComponent, _Component);

  function TestComponent() {
    _classCallCheck(this, TestComponent);

    return _possibleConstructorReturn(this, _getPrototypeOf(TestComponent).apply(this, arguments));
  }

  _createClass(TestComponent, [{
    key: "render",
    value: function render() {
      return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        id: this.props.id
      }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "array"
      }, this.props.array_prop && JSON.stringify(this.props.array_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "bool"
      }, Object(ramda__WEBPACK_IMPORTED_MODULE_2__["isNil"])(this.props.bool_prop) ? '' : this.props.bool_prop ? 'True' : 'False'), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "number"
      }, this.props.number_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "object"
      }, this.props.object_prop && JSON.stringify(this.props.object_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "string"
      }, this.props.string_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "symbol"
      }, this.props.symbol_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "enum"
      }, this.props.enum_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "union"
      }, this.props.union_prop), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "array_of"
      }, this.props.array_of_prop && JSON.stringify(this.props.array_of_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "object_of"
      }, this.props.object_of_prop && JSON.stringify(this.props.object_of_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "shape"
      }, this.props.shape_prop && JSON.stringify(this.props.shape_prop)), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
        className: "required_string"
      }, this.props.required_string));
    }
  }]);

  return TestComponent;
}(react__WEBPACK_IMPORTED_MODULE_0__["Component"]);


TestComponent.defaultProps = {
  string_with_default: 'Foo'
};
TestComponent.propTypes = {
  /**
   * The ID used to identify this component in the DOM.
   * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
   */
  id: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Array props with
   */
  array_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  bool_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  func_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func,
  number_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
  object_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.object,
  string_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  symbol_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.symbol,
  any_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.any,
  string_with_default: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  enum_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOf(['News', 'Photos']),
  // An object that could be one of many types
  union_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.oneOfType([prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string, prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number]),
  // An array of a certain type
  array_of_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number),
  // An object with property values of a certain type
  object_of_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.objectOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number),
  // An object taking on a particular shape
  shape_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
    color: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
    fontSize: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number
  }),
  required_string: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,
  // These don't work good.
  nested_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
    string_prop: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
    nested_shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
      nested_array: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
        nested_array_string: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
        nested_array_shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
          prop1: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
          prop2: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string
        })
      })),
      nested_shape_shape: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.shape({
        prop3: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number,
        prop4: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool
      })
    })
  }),
  array_of_array: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.arrayOf(prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.number)),
  children: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.node,
  identity: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,
  updateAspects: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ }),

/***/ "./src/internal/test_components/index.js":
/*!***********************************************!*\
  !*** ./src/internal/test_components/index.js ***!
  \***********************************************/
/*! exports provided: TestComponent, DefaultProps, ComponentAsAspect */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _components_TestComponent__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components/TestComponent */ "./src/internal/test_components/components/TestComponent.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "TestComponent", function() { return _components_TestComponent__WEBPACK_IMPORTED_MODULE_0__["default"]; });

/* harmony import */ var _components_DefaultProps__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/DefaultProps */ "./src/internal/test_components/components/DefaultProps.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "DefaultProps", function() { return _components_DefaultProps__WEBPACK_IMPORTED_MODULE_1__["default"]; });

/* harmony import */ var _components_ComponentAsAspect__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/ComponentAsAspect */ "./src/internal/test_components/components/ComponentAsAspect.jsx");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "ComponentAsAspect", function() { return _components_ComponentAsAspect__WEBPACK_IMPORTED_MODULE_2__["default"]; });






/***/ }),

/***/ 2:
/*!*****************************************************!*\
  !*** multi ./src/internal/test_components/index.js ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/t4rk/projects/experiments/dazzler/src/internal/test_components/index.js */"./src/internal/test_components/index.js");


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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8uL3NyYy9pbnRlcm5hbC90ZXN0X2NvbXBvbmVudHMvY29tcG9uZW50cy9Db21wb25lbnRBc0FzcGVjdC5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9pbnRlcm5hbC90ZXN0X2NvbXBvbmVudHMvY29tcG9uZW50cy9EZWZhdWx0UHJvcHMuanN4PyIsIndlYnBhY2s6Ly8vLi9zcmMvaW50ZXJuYWwvdGVzdF9jb21wb25lbnRzL2NvbXBvbmVudHMvVGVzdENvbXBvbmVudC5qc3g/Iiwid2VicGFjazovLy8uL3NyYy9pbnRlcm5hbC90ZXN0X2NvbXBvbmVudHMvaW5kZXguanM/Iiwid2VicGFjazovLy9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3RcIixcImNvbW1vbmpzMlwiOlwicmVhY3RcIixcImFtZFwiOlwicmVhY3RcIixcInVtZFwiOlwicmVhY3RcIixcInJvb3RcIjpcIlJlYWN0XCJ9PyJdLCJuYW1lcyI6WyJDb21wb25lbnRBc0FzcGVjdCIsInByb3BzIiwiaWRlbnRpdHkiLCJzaW5nbGUiLCJhcnJheSIsInNoYXBlIiwibWFwIiwiZSIsImkiLCJzaGFwZWQiLCJSZWFjdCIsIkNvbXBvbmVudCIsImRlZmF1bHRQcm9wcyIsInByb3BUeXBlcyIsIlByb3BUeXBlcyIsImVsZW1lbnQiLCJhcnJheU9mIiwic3RyaW5nIiwidXBkYXRlQXNwZWN0cyIsImZ1bmMiLCJEZWZhdWx0UHJvcHMiLCJpZCIsIk9iamVjdCIsImVudHJpZXMiLCJrIiwidiIsIkpTT04iLCJzdHJpbmdpZnkiLCJzdHJpbmdfZGVmYXVsdCIsInN0cmluZ19kZWZhdWx0X2VtcHR5IiwibnVtYmVyX2RlZmF1bHQiLCJudW1iZXJfZGVmYXVsdF9lbXB0eSIsImFycmF5X2RlZmF1bHQiLCJhcnJheV9kZWZhdWx0X2VtcHR5Iiwib2JqZWN0X2RlZmF1bHQiLCJmb28iLCJvYmplY3RfZGVmYXVsdF9lbXB0eSIsIm51bWJlciIsIm9iamVjdCIsIlRlc3RDb21wb25lbnQiLCJhcnJheV9wcm9wIiwiaXNOaWwiLCJib29sX3Byb3AiLCJudW1iZXJfcHJvcCIsIm9iamVjdF9wcm9wIiwic3RyaW5nX3Byb3AiLCJzeW1ib2xfcHJvcCIsImVudW1fcHJvcCIsInVuaW9uX3Byb3AiLCJhcnJheV9vZl9wcm9wIiwib2JqZWN0X29mX3Byb3AiLCJzaGFwZV9wcm9wIiwicmVxdWlyZWRfc3RyaW5nIiwic3RyaW5nX3dpdGhfZGVmYXVsdCIsImJvb2wiLCJmdW5jX3Byb3AiLCJzeW1ib2wiLCJhbnlfcHJvcCIsImFueSIsIm9uZU9mIiwib25lT2ZUeXBlIiwib2JqZWN0T2YiLCJjb2xvciIsImZvbnRTaXplIiwiaXNSZXF1aXJlZCIsIm5lc3RlZF9wcm9wIiwibmVzdGVkX3NoYXBlIiwibmVzdGVkX2FycmF5IiwibmVzdGVkX2FycmF5X3N0cmluZyIsIm5lc3RlZF9hcnJheV9zaGFwZSIsInByb3AxIiwicHJvcDIiLCJuZXN0ZWRfc2hhcGVfc2hhcGUiLCJwcm9wMyIsInByb3A0IiwiYXJyYXlfb2ZfYXJyYXkiLCJjaGlsZHJlbiIsIm5vZGUiXSwibWFwcGluZ3MiOiJBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLENBQUM7QUFDRCxPO0FDVkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxnQkFBUSxvQkFBb0I7QUFDNUI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx5QkFBaUIsNEJBQTRCO0FBQzdDO0FBQ0E7QUFDQSwwQkFBa0IsMkJBQTJCO0FBQzdDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FB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QVMsQ0FBQ0UsT0FBVixDQUFrQkYsaURBQVMsQ0FBQ3VCLE1BQTVCLENBQWxCLENBMURNO0FBNER0QnVDLFVBQVEsRUFBRTlELGlEQUFTLENBQUMrRCxJQTVERTtBQTZEdEIzRSxVQUFRLEVBQUVZLGlEQUFTLENBQUNHLE1BN0RFO0FBOER0QkMsZUFBYSxFQUFFSixpREFBUyxDQUFDSztBQTlESCxDQUExQixDOzs7Ozs7Ozs7Ozs7QUN4REE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUNBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ0ZBLG1EIiwiZmlsZSI6ImRhenpsZXJfdGVzdF8zOTViNDFlZmI0YzA5ZjI1YjljNy5qcyIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfdGVzdFwiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX3Rlc3RcIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KSh3aW5kb3csIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsIiBcdC8vIGluc3RhbGwgYSBKU09OUCBjYWxsYmFjayBmb3IgY2h1bmsgbG9hZGluZ1xuIFx0ZnVuY3Rpb24gd2VicGFja0pzb25wQ2FsbGJhY2soZGF0YSkge1xuIFx0XHR2YXIgY2h1bmtJZHMgPSBkYXRhWzBdO1xuIFx0XHR2YXIgbW9yZU1vZHVsZXMgPSBkYXRhWzFdO1xuIFx0XHR2YXIgZXhlY3V0ZU1vZHVsZXMgPSBkYXRhWzJdO1xuXG4gXHRcdC8vIGFkZCBcIm1vcmVNb2R1bGVzXCIgdG8gdGhlIG1vZHVsZXMgb2JqZWN0LFxuIFx0XHQvLyB0aGVuIGZsYWcgYWxsIFwiY2h1bmtJZHNcIiBhcyBsb2FkZWQgYW5kIGZpcmUgY2FsbGJhY2tcbiBcdFx0dmFyIG1vZHVsZUlkLCBjaHVua0lkLCBpID0gMCwgcmVzb2x2ZXMgPSBbXTtcbiBcdFx0Zm9yKDtpIDwgY2h1bmtJZHMubGVuZ3RoOyBpKyspIHtcbiBcdFx0XHRjaHVua0lkID0gY2h1bmtJZHNbaV07XG4gXHRcdFx0aWYoaW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdKSB7XG4gXHRcdFx0XHRyZXNvbHZlcy5wdXNoKGluc3RhbGxlZENodW5rc1tjaHVua0lkXVswXSk7XG4gXHRcdFx0fVxuIFx0XHRcdGluc3RhbGxlZENodW5rc1tjaHVua0lkXSA9IDA7XG4gXHRcdH1cbiBcdFx0Zm9yKG1vZHVsZUlkIGluIG1vcmVNb2R1bGVzKSB7XG4gXHRcdFx0aWYoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG1vcmVNb2R1bGVzLCBtb2R1bGVJZCkpIHtcbiBcdFx0XHRcdG1vZHVsZXNbbW9kdWxlSWRdID0gbW9yZU1vZHVsZXNbbW9kdWxlSWRdO1xuIFx0XHRcdH1cbiBcdFx0fVxuIFx0XHRpZihwYXJlbnRKc29ucEZ1bmN0aW9uKSBwYXJlbnRKc29ucEZ1bmN0aW9uKGRhdGEpO1xuXG4gXHRcdHdoaWxlKHJlc29sdmVzLmxlbmd0aCkge1xuIFx0XHRcdHJlc29sdmVzLnNoaWZ0KCkoKTtcbiBcdFx0fVxuXG4gXHRcdC8vIGFkZCBlbnRyeSBtb2R1bGVzIGZyb20gbG9hZGVkIGNodW5rIHRvIGRlZmVycmVkIGxpc3RcbiBcdFx0ZGVmZXJyZWRNb2R1bGVzLnB1c2guYXBwbHkoZGVmZXJyZWRNb2R1bGVzLCBleGVjdXRlTW9kdWxlcyB8fCBbXSk7XG5cbiBcdFx0Ly8gcnVuIGRlZmVycmVkIG1vZHVsZXMgd2hlbiBhbGwgY2h1bmtzIHJlYWR5XG4gXHRcdHJldHVybiBjaGVja0RlZmVycmVkTW9kdWxlcygpO1xuIFx0fTtcbiBcdGZ1bmN0aW9uIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCkge1xuIFx0XHR2YXIgcmVzdWx0O1xuIFx0XHRmb3IodmFyIGkgPSAwOyBpIDwgZGVmZXJyZWRNb2R1bGVzLmxlbmd0aDsgaSsrKSB7XG4gXHRcdFx0dmFyIGRlZmVycmVkTW9kdWxlID0gZGVmZXJyZWRNb2R1bGVzW2ldO1xuIFx0XHRcdHZhciBmdWxmaWxsZWQgPSB0cnVlO1xuIFx0XHRcdGZvcih2YXIgaiA9IDE7IGogPCBkZWZlcnJlZE1vZHVsZS5sZW5ndGg7IGorKykge1xuIFx0XHRcdFx0dmFyIGRlcElkID0gZGVmZXJyZWRNb2R1bGVbal07XG4gXHRcdFx0XHRpZihpbnN0YWxsZWRDaHVua3NbZGVwSWRdICE9PSAwKSBmdWxmaWxsZWQgPSBmYWxzZTtcbiBcdFx0XHR9XG4gXHRcdFx0aWYoZnVsZmlsbGVkKSB7XG4gXHRcdFx0XHRkZWZlcnJlZE1vZHVsZXMuc3BsaWNlKGktLSwgMSk7XG4gXHRcdFx0XHRyZXN1bHQgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IGRlZmVycmVkTW9kdWxlWzBdKTtcbiBcdFx0XHR9XG4gXHRcdH1cblxuIFx0XHRyZXR1cm4gcmVzdWx0O1xuIFx0fVxuXG4gXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBvYmplY3QgdG8gc3RvcmUgbG9hZGVkIGFuZCBsb2FkaW5nIGNodW5rc1xuIFx0Ly8gdW5kZWZpbmVkID0gY2h1bmsgbm90IGxvYWRlZCwgbnVsbCA9IGNodW5rIHByZWxvYWRlZC9wcmVmZXRjaGVkXG4gXHQvLyBQcm9taXNlID0gY2h1bmsgbG9hZGluZywgMCA9IGNodW5rIGxvYWRlZFxuIFx0dmFyIGluc3RhbGxlZENodW5rcyA9IHtcbiBcdFx0XCJ0ZXN0XCI6IDBcbiBcdH07XG5cbiBcdHZhciBkZWZlcnJlZE1vZHVsZXMgPSBbXTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuIFx0dmFyIGpzb25wQXJyYXkgPSB3aW5kb3dbXCJ3ZWJwYWNrSnNvbnBkYXp6bGVyX25hbWVfXCJdID0gd2luZG93W1wid2VicGFja0pzb25wZGF6emxlcl9uYW1lX1wiXSB8fCBbXTtcbiBcdHZhciBvbGRKc29ucEZ1bmN0aW9uID0ganNvbnBBcnJheS5wdXNoLmJpbmQoanNvbnBBcnJheSk7XG4gXHRqc29ucEFycmF5LnB1c2ggPSB3ZWJwYWNrSnNvbnBDYWxsYmFjaztcbiBcdGpzb25wQXJyYXkgPSBqc29ucEFycmF5LnNsaWNlKCk7XG4gXHRmb3IodmFyIGkgPSAwOyBpIDwganNvbnBBcnJheS5sZW5ndGg7IGkrKykgd2VicGFja0pzb25wQ2FsbGJhY2soanNvbnBBcnJheVtpXSk7XG4gXHR2YXIgcGFyZW50SnNvbnBGdW5jdGlvbiA9IG9sZEpzb25wRnVuY3Rpb247XG5cblxuIFx0Ly8gYWRkIGVudHJ5IG1vZHVsZSB0byBkZWZlcnJlZCBsaXN0XG4gXHRkZWZlcnJlZE1vZHVsZXMucHVzaChbMixcImNvbW1vbnNcIl0pO1xuIFx0Ly8gcnVuIGRlZmVycmVkIG1vZHVsZXMgd2hlbiByZWFkeVxuIFx0cmV0dXJuIGNoZWNrRGVmZXJyZWRNb2R1bGVzKCk7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgQ29tcG9uZW50QXNBc3BlY3QgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQge1xuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge2lkZW50aXR5LCBzaW5nbGUsIGFycmF5LCBzaGFwZX0gPSB0aGlzLnByb3BzO1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBpZD17aWRlbnRpdHl9PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwic2luZ2xlXCI+e3NpbmdsZX08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImFycmF5XCI+XG4gICAgICAgICAgICAgICAgICAgIHthcnJheS5tYXAoKGUsIGkpID0+IChcbiAgICAgICAgICAgICAgICAgICAgICAgIDxkaXYga2V5PXtpfT57ZX08L2Rpdj5cbiAgICAgICAgICAgICAgICAgICAgKSl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzaGFwZVwiPntzaGFwZS5zaGFwZWR9PC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICB9XG59XG5cbkNvbXBvbmVudEFzQXNwZWN0LmRlZmF1bHRQcm9wcyA9IHt9O1xuXG5Db21wb25lbnRBc0FzcGVjdC5wcm9wVHlwZXMgPSB7XG4gICAgc2luZ2xlOiBQcm9wVHlwZXMuZWxlbWVudCxcbiAgICBhcnJheTogUHJvcFR5cGVzLmFycmF5T2YoUHJvcFR5cGVzLmVsZW1lbnQpLFxuICAgIHNoYXBlOiBQcm9wVHlwZXMuc2hhcGUoe1xuICAgICAgICBzaGFwZWQ6IFByb3BUeXBlcy5lbGVtZW50LFxuICAgIH0pLFxuXG4gICAgLyoqXG4gICAgICogIFVuaXF1ZSBpZCBmb3IgdGhpcyBjb21wb25lbnRcbiAgICAgKi9cbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIC8qKlxuICAgICAqIFVwZGF0ZSBhc3BlY3RzIG9uIHRoZSBiYWNrZW5kLlxuICAgICAqL1xuICAgIHVwZGF0ZUFzcGVjdHM6IFByb3BUeXBlcy5mdW5jLFxufTtcbiIsImltcG9ydCBSZWFjdCwge0NvbXBvbmVudH0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IFByb3BUeXBlcyBmcm9tICdwcm9wLXR5cGVzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgRGVmYXVsdFByb3BzIGV4dGVuZHMgQ29tcG9uZW50IHtcbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtpZH0gPSB0aGlzLnByb3BzO1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBpZD17aWR9PlxuICAgICAgICAgICAgICAgIHtPYmplY3QuZW50cmllcyh0aGlzLnByb3BzKS5tYXAoKGssIHYpID0+IChcbiAgICAgICAgICAgICAgICAgICAgPGRpdiBpZD17YCR7aWR9LSR7a31gfSBrZXk9e2Ake2lkfS0ke2t9YH0+XG4gICAgICAgICAgICAgICAgICAgICAgICB7a306IHtKU09OLnN0cmluZ2lmeSh2KX1cbiAgICAgICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgKSl9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICB9XG59XG5cbkRlZmF1bHRQcm9wcy5kZWZhdWx0UHJvcHMgPSB7XG4gICAgc3RyaW5nX2RlZmF1bHQ6ICdEZWZhdWx0IHN0cmluZycsXG4gICAgc3RyaW5nX2RlZmF1bHRfZW1wdHk6ICcnLFxuICAgIG51bWJlcl9kZWZhdWx0OiAwLjI2NjYsXG4gICAgbnVtYmVyX2RlZmF1bHRfZW1wdHk6IDAsXG4gICAgYXJyYXlfZGVmYXVsdDogWzEsIDIsIDNdLFxuICAgIGFycmF5X2RlZmF1bHRfZW1wdHk6IFtdLFxuICAgIG9iamVjdF9kZWZhdWx0OiB7Zm9vOiAnYmFyJ30sXG4gICAgb2JqZWN0X2RlZmF1bHRfZW1wdHk6IHt9LFxufTtcblxuRGVmYXVsdFByb3BzLnByb3BUeXBlcyA9IHtcbiAgICBpZDogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIHN0cmluZ19kZWZhdWx0OiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgIHN0cmluZ19kZWZhdWx0X2VtcHR5OiBQcm9wVHlwZXMuc3RyaW5nLFxuXG4gICAgbnVtYmVyX2RlZmF1bHQ6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgbnVtYmVyX2RlZmF1bHRfZW1wdHk6IFByb3BUeXBlcy5udW1iZXIsXG5cbiAgICBhcnJheV9kZWZhdWx0OiBQcm9wVHlwZXMuYXJyYXksXG4gICAgYXJyYXlfZGVmYXVsdF9lbXB0eTogUHJvcFR5cGVzLmFycmF5LFxuXG4gICAgb2JqZWN0X2RlZmF1bHQ6IFByb3BUeXBlcy5vYmplY3QsXG4gICAgb2JqZWN0X2RlZmF1bHRfZW1wdHk6IFByb3BUeXBlcy5vYmplY3QsXG59O1xuIiwiaW1wb3J0IFJlYWN0LCB7Q29tcG9uZW50fSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgUHJvcFR5cGVzIGZyb20gJ3Byb3AtdHlwZXMnO1xuaW1wb3J0IHtpc05pbH0gZnJvbSAncmFtZGEnO1xuXG4vKipcbiAqIFRlc3QgY29tcG9uZW50IHdpdGggYWxsIHN1cHBvcnRlZCBwcm9wcyBieSBkYXp6bGVyLlxuICogRWFjaCBwcm9wIGFyZSByZW5kZXJlZCB3aXRoIGEgc2VsZWN0b3IgZm9yIGVhc3kgYWNjZXNzLlxuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBUZXN0Q29tcG9uZW50IGV4dGVuZHMgQ29tcG9uZW50IHtcbiAgICByZW5kZXIoKSB7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGlkPXt0aGlzLnByb3BzLmlkfT5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImFycmF5XCI+XG4gICAgICAgICAgICAgICAgICAgIHt0aGlzLnByb3BzLmFycmF5X3Byb3AgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHRoaXMucHJvcHMuYXJyYXlfcHJvcCl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJib29sXCI+XG4gICAgICAgICAgICAgICAgICAgIHtpc05pbCh0aGlzLnByb3BzLmJvb2xfcHJvcClcbiAgICAgICAgICAgICAgICAgICAgICAgID8gJydcbiAgICAgICAgICAgICAgICAgICAgICAgIDogdGhpcy5wcm9wcy5ib29sX3Byb3BcbiAgICAgICAgICAgICAgICAgICAgICAgID8gJ1RydWUnXG4gICAgICAgICAgICAgICAgICAgICAgICA6ICdGYWxzZSd9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJudW1iZXJcIj57dGhpcy5wcm9wcy5udW1iZXJfcHJvcH08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cIm9iamVjdFwiPlxuICAgICAgICAgICAgICAgICAgICB7dGhpcy5wcm9wcy5vYmplY3RfcHJvcCAmJlxuICAgICAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkodGhpcy5wcm9wcy5vYmplY3RfcHJvcCl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJzdHJpbmdcIj57dGhpcy5wcm9wcy5zdHJpbmdfcHJvcH08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInN5bWJvbFwiPnt0aGlzLnByb3BzLnN5bWJvbF9wcm9wfTwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZW51bVwiPnt0aGlzLnByb3BzLmVudW1fcHJvcH08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInVuaW9uXCI+e3RoaXMucHJvcHMudW5pb25fcHJvcH08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImFycmF5X29mXCI+XG4gICAgICAgICAgICAgICAgICAgIHt0aGlzLnByb3BzLmFycmF5X29mX3Byb3AgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHRoaXMucHJvcHMuYXJyYXlfb2ZfcHJvcCl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJvYmplY3Rfb2ZcIj5cbiAgICAgICAgICAgICAgICAgICAge3RoaXMucHJvcHMub2JqZWN0X29mX3Byb3AgJiZcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHRoaXMucHJvcHMub2JqZWN0X29mX3Byb3ApfVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwic2hhcGVcIj5cbiAgICAgICAgICAgICAgICAgICAge3RoaXMucHJvcHMuc2hhcGVfcHJvcCAmJlxuICAgICAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkodGhpcy5wcm9wcy5zaGFwZV9wcm9wKX1cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInJlcXVpcmVkX3N0cmluZ1wiPlxuICAgICAgICAgICAgICAgICAgICB7dGhpcy5wcm9wcy5yZXF1aXJlZF9zdHJpbmd9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICB9XG59XG5cblRlc3RDb21wb25lbnQuZGVmYXVsdFByb3BzID0ge1xuICAgIHN0cmluZ193aXRoX2RlZmF1bHQ6ICdGb28nLFxufTtcblxuVGVzdENvbXBvbmVudC5wcm9wVHlwZXMgPSB7XG4gICAgLyoqXG4gICAgICogVGhlIElEIHVzZWQgdG8gaWRlbnRpZnkgdGhpcyBjb21wb25lbnQgaW4gdGhlIERPTS5cbiAgICAgKiBMb3JlbSBpcHN1bSBkb2xvciBzaXQgYW1ldCwgY29uc2VjdGV0dXIgYWRpcGlzY2luZyBlbGl0LCBzZWQgZG8gZWl1c21vZCB0ZW1wb3IgaW5jaWRpZHVudCB1dCBsYWJvcmUgZXQgZG9sb3JlIG1hZ25hIGFsaXF1YS4gVXQgZW5pbSBhZCBtaW5pbSB2ZW5pYW0sIHF1aXMgbm9zdHJ1ZCBleGVyY2l0YXRpb24gdWxsYW1jbyBsYWJvcmlzIG5pc2kgdXQgYWxpcXVpcCBleCBlYSBjb21tb2RvIGNvbnNlcXVhdC4gRHVpcyBhdXRlIGlydXJlIGRvbG9yIGluIHJlcHJlaGVuZGVyaXQgaW4gdm9sdXB0YXRlIHZlbGl0IGVzc2UgY2lsbHVtIGRvbG9yZSBldSBmdWdpYXQgbnVsbGEgcGFyaWF0dXIuIEV4Y2VwdGV1ciBzaW50IG9jY2FlY2F0IGN1cGlkYXRhdCBub24gcHJvaWRlbnQsIHN1bnQgaW4gY3VscGEgcXVpIG9mZmljaWEgZGVzZXJ1bnQgbW9sbGl0IGFuaW0gaWQgZXN0IGxhYm9ydW0uXG4gICAgICovXG4gICAgaWQ6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBBcnJheSBwcm9wcyB3aXRoXG4gICAgICovXG4gICAgYXJyYXlfcHJvcDogUHJvcFR5cGVzLmFycmF5LFxuICAgIGJvb2xfcHJvcDogUHJvcFR5cGVzLmJvb2wsXG4gICAgZnVuY19wcm9wOiBQcm9wVHlwZXMuZnVuYyxcbiAgICBudW1iZXJfcHJvcDogUHJvcFR5cGVzLm51bWJlcixcbiAgICBvYmplY3RfcHJvcDogUHJvcFR5cGVzLm9iamVjdCxcbiAgICBzdHJpbmdfcHJvcDogUHJvcFR5cGVzLnN0cmluZyxcbiAgICBzeW1ib2xfcHJvcDogUHJvcFR5cGVzLnN5bWJvbCxcbiAgICBhbnlfcHJvcDogUHJvcFR5cGVzLmFueSxcblxuICAgIHN0cmluZ193aXRoX2RlZmF1bHQ6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgZW51bV9wcm9wOiBQcm9wVHlwZXMub25lT2YoWydOZXdzJywgJ1Bob3RvcyddKSxcblxuICAgIC8vIEFuIG9iamVjdCB0aGF0IGNvdWxkIGJlIG9uZSBvZiBtYW55IHR5cGVzXG4gICAgdW5pb25fcHJvcDogUHJvcFR5cGVzLm9uZU9mVHlwZShbUHJvcFR5cGVzLnN0cmluZywgUHJvcFR5cGVzLm51bWJlcl0pLFxuXG4gICAgLy8gQW4gYXJyYXkgb2YgYSBjZXJ0YWluIHR5cGVcbiAgICBhcnJheV9vZl9wcm9wOiBQcm9wVHlwZXMuYXJyYXlPZihQcm9wVHlwZXMubnVtYmVyKSxcblxuICAgIC8vIEFuIG9iamVjdCB3aXRoIHByb3BlcnR5IHZhbHVlcyBvZiBhIGNlcnRhaW4gdHlwZVxuICAgIG9iamVjdF9vZl9wcm9wOiBQcm9wVHlwZXMub2JqZWN0T2YoUHJvcFR5cGVzLm51bWJlciksXG5cbiAgICAvLyBBbiBvYmplY3QgdGFraW5nIG9uIGEgcGFydGljdWxhciBzaGFwZVxuICAgIHNoYXBlX3Byb3A6IFByb3BUeXBlcy5zaGFwZSh7XG4gICAgICAgIGNvbG9yOiBQcm9wVHlwZXMuc3RyaW5nLFxuICAgICAgICBmb250U2l6ZTogUHJvcFR5cGVzLm51bWJlcixcbiAgICB9KSxcbiAgICByZXF1aXJlZF9zdHJpbmc6IFByb3BUeXBlcy5zdHJpbmcuaXNSZXF1aXJlZCxcblxuICAgIC8vIFRoZXNlIGRvbid0IHdvcmsgZ29vZC5cbiAgICBuZXN0ZWRfcHJvcDogUHJvcFR5cGVzLnNoYXBlKHtcbiAgICAgICAgc3RyaW5nX3Byb3A6IFByb3BUeXBlcy5zdHJpbmcsXG4gICAgICAgIG5lc3RlZF9zaGFwZTogUHJvcFR5cGVzLnNoYXBlKHtcbiAgICAgICAgICAgIG5lc3RlZF9hcnJheTogUHJvcFR5cGVzLmFycmF5T2YoXG4gICAgICAgICAgICAgICAgUHJvcFR5cGVzLnNoYXBlKHtcbiAgICAgICAgICAgICAgICAgICAgbmVzdGVkX2FycmF5X3N0cmluZzogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAgICAgICAgICAgICAgICAgbmVzdGVkX2FycmF5X3NoYXBlOiBQcm9wVHlwZXMuc2hhcGUoe1xuICAgICAgICAgICAgICAgICAgICAgICAgcHJvcDE6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgICAgICAgICAgICAgICAgICAgICBwcm9wMjogUHJvcFR5cGVzLnN0cmluZyxcbiAgICAgICAgICAgICAgICAgICAgfSksXG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICksXG4gICAgICAgICAgICBuZXN0ZWRfc2hhcGVfc2hhcGU6IFByb3BUeXBlcy5zaGFwZSh7XG4gICAgICAgICAgICAgICAgcHJvcDM6IFByb3BUeXBlcy5udW1iZXIsXG4gICAgICAgICAgICAgICAgcHJvcDQ6IFByb3BUeXBlcy5ib29sLFxuICAgICAgICAgICAgfSksXG4gICAgICAgIH0pLFxuICAgIH0pLFxuXG4gICAgYXJyYXlfb2ZfYXJyYXk6IFByb3BUeXBlcy5hcnJheU9mKFByb3BUeXBlcy5hcnJheU9mKFByb3BUeXBlcy5udW1iZXIpKSxcblxuICAgIGNoaWxkcmVuOiBQcm9wVHlwZXMubm9kZSxcbiAgICBpZGVudGl0eTogUHJvcFR5cGVzLnN0cmluZyxcbiAgICB1cGRhdGVBc3BlY3RzOiBQcm9wVHlwZXMuZnVuYyxcbn07XG4iLCJpbXBvcnQgVGVzdENvbXBvbmVudCBmcm9tICcuL2NvbXBvbmVudHMvVGVzdENvbXBvbmVudCc7XG5pbXBvcnQgRGVmYXVsdFByb3BzIGZyb20gJy4vY29tcG9uZW50cy9EZWZhdWx0UHJvcHMnO1xuaW1wb3J0IENvbXBvbmVudEFzQXNwZWN0IGZyb20gJy4vY29tcG9uZW50cy9Db21wb25lbnRBc0FzcGVjdCc7XG5cbmV4cG9ydCB7VGVzdENvbXBvbmVudCwgRGVmYXVsdFByb3BzLCBDb21wb25lbnRBc0FzcGVjdH07XG4iLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiXSwic291cmNlUm9vdCI6IiJ9
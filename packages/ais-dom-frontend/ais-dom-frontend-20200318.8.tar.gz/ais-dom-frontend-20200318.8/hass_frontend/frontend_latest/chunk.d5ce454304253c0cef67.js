/*! For license information please see chunk.d5ce454304253c0cef67.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[171,11,161,162,163,164,165,167,168,169,172],{103:function(t,e,n){"use strict";n.d(e,"a",function(){return a});n(3);var r=n(5),i=n(4);const a=Object(r.a)({_template:i.a`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},_text:{type:String,value:""}},created:function(){a.instance||(a.instance=this),document.body.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(t){this._text="",this.async(function(){this._text=t},100)},_onIronAnnounce:function(t){t.detail&&t.detail.text&&this.announce(t.detail.text)}});a.instance=null,a.requestAvailability=function(){a.instance||(a.instance=document.createElement("iron-a11y-announcer")),document.body.appendChild(a.instance)}},124:function(t,e,n){"use strict";n(3);var r=n(103),i=n(65),a=n(5),o=n(1),s=n(4);Object(a.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[i.a],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){r.a.requestAvailability(),this._previousValidInput="",this._patternAlreadyChecked=!1},attached:function(){this._observer=Object(o.a)(this).observeNodes(function(t){this._initSlottedInput()}.bind(this))},detached:function(){this._observer&&(Object(o.a)(this).unobserveNodes(this._observer),this._observer=null)},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0],this.inputElement&&this.inputElement.value&&(this.bindValue=this.inputElement.value),this.fire("iron-input-ready")},get _patternRegExp(){var t;if(this.allowedPattern)t=new RegExp(this.allowedPattern);else switch(this.inputElement.type){case"number":t=/[0-9.,e-]/}return t},_bindValueChanged:function(t,e){e&&(void 0===t?e.value=null:t!==e.value&&(this.inputElement.value=t),this.autoValidate&&this.validate(),this.fire("bind-value-changed",{value:t}))},_onInput:function(){this.allowedPattern&&!this._patternAlreadyChecked&&(this._checkPatternValidity()||(this._announceInvalidCharacter("Invalid string of characters not entered."),this.inputElement.value=this._previousValidInput));this.bindValue=this._previousValidInput=this.inputElement.value,this._patternAlreadyChecked=!1},_isPrintable:function(t){var e=8==t.keyCode||9==t.keyCode||13==t.keyCode||27==t.keyCode,n=19==t.keyCode||20==t.keyCode||45==t.keyCode||46==t.keyCode||144==t.keyCode||145==t.keyCode||t.keyCode>32&&t.keyCode<41||t.keyCode>111&&t.keyCode<124;return!(e||0==t.charCode&&n)},_onKeypress:function(t){if(this.allowedPattern||"number"===this.inputElement.type){var e=this._patternRegExp;if(e&&!(t.metaKey||t.ctrlKey||t.altKey)){this._patternAlreadyChecked=!0;var n=String.fromCharCode(t.charCode);this._isPrintable(t)&&!e.test(n)&&(t.preventDefault(),this._announceInvalidCharacter("Invalid character "+n+" not entered."))}}},_checkPatternValidity:function(){var t=this._patternRegExp;if(!t)return!0;for(var e=0;e<this.inputElement.value.length;e++)if(!t.test(this.inputElement.value[e]))return!1;return!0},validate:function(){if(!this.inputElement)return this.invalid=!1,!0;var t=this.inputElement.checkValidity();return t&&(this.required&&""===this.bindValue?t=!1:this.hasValidator()&&(t=i.a.validate.call(this,this.bindValue))),this.invalid=!t,this.fire("iron-input-validate"),t},_announceInvalidCharacter:function(t){this.fire("iron-announce",{text:t})},_computeValue:function(t){return t}})},132:function(t,e,n){"use strict";var r=function(t,e){return t.length===e.length&&t.every(function(t,n){return r=t,i=e[n],r===i;var r,i})};e.a=function(t,e){var n;void 0===e&&(e=r);var i,a=[],o=!1;return function(){for(var r=arguments.length,s=new Array(r),l=0;l<r;l++)s[l]=arguments[l];return o&&n===this&&e(s,a)?i:(i=t.apply(this,s),o=!0,n=this,a=s,i)}}},158:function(t,e,n){"use strict";n(3),n(51),n(52),n(134);var r=n(5),i=n(4),a=n(121);Object(r.a)({_template:i.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[a.a]})},193:function(t,e,n){"use strict";n(3),n(51),n(47),n(52);var r=n(5),i=n(4);Object(r.a)({_template:i.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},217:function(t,e,n){"use strict";n.d(e,"a",function(){return i});n(3);var r=n(1);const i={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(t,e){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),e)if("document"===t)this.scrollTarget=this._doc;else if("string"==typeof t){var n=this.domHost;this.scrollTarget=n&&n.$?n.$[t]:Object(r.a)(this.ownerDocument).querySelector("#"+t)}else this._isValidScrollTarget()&&(this._oldScrollTarget=t,this._toggleScrollListener(this._shouldHaveListener,t))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(t){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=t)},set _scrollLeft(t){this.scrollTarget===this._doc?window.scrollTo(t,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=t)},scroll:function(t,e){var n;"object"==typeof t?(n=t.left,e=t.top):n=t,n=n||0,e=e||0,this.scrollTarget===this._doc?window.scrollTo(n,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=n,this.scrollTarget.scrollTop=e)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(t,e){var n=e===this._doc?window:e;t?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),n.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(n.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(t){this._shouldHaveListener=t,this._toggleScrollListener(t,this.scrollTarget)}}},221:function(t,e,n){"use strict";n.d(e,"a",function(){return T});class r extends TypeError{static format(t){const{type:e,path:n,value:r}=t;return`Expected a value of type \`${e}\`${n.length?` for \`${n.join(".")}\``:""} but received \`${JSON.stringify(r)}\`.`}constructor(t){super(r.format(t));const{data:e,path:n,value:i,reason:a,type:o,errors:s=[]}=t;this.data=e,this.path=n,this.value=i,this.reason=a,this.type=o,this.errors=s,s.length||s.push(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=(new Error).stack}}var i=Object.prototype.toString,a=function(t){if(void 0===t)return"undefined";if(null===t)return"null";var e=typeof t;if("boolean"===e)return"boolean";if("string"===e)return"string";if("number"===e)return"number";if("symbol"===e)return"symbol";if("function"===e)return"GeneratorFunction"===o(t)?"generatorfunction":"function";if(function(t){return Array.isArray?Array.isArray(t):t instanceof Array}(t))return"array";if(function(t){if(t.constructor&&"function"==typeof t.constructor.isBuffer)return t.constructor.isBuffer(t);return!1}(t))return"buffer";if(function(t){try{if("number"==typeof t.length&&"function"==typeof t.callee)return!0}catch(e){if(-1!==e.message.indexOf("callee"))return!0}return!1}(t))return"arguments";if(function(t){return t instanceof Date||"function"==typeof t.toDateString&&"function"==typeof t.getDate&&"function"==typeof t.setDate}(t))return"date";if(function(t){return t instanceof Error||"string"==typeof t.message&&t.constructor&&"number"==typeof t.constructor.stackTraceLimit}(t))return"error";if(function(t){return t instanceof RegExp||"string"==typeof t.flags&&"boolean"==typeof t.ignoreCase&&"boolean"==typeof t.multiline&&"boolean"==typeof t.global}(t))return"regexp";switch(o(t)){case"Symbol":return"symbol";case"Promise":return"promise";case"WeakMap":return"weakmap";case"WeakSet":return"weakset";case"Map":return"map";case"Set":return"set";case"Int8Array":return"int8array";case"Uint8Array":return"uint8array";case"Uint8ClampedArray":return"uint8clampedarray";case"Int16Array":return"int16array";case"Uint16Array":return"uint16array";case"Int32Array":return"int32array";case"Uint32Array":return"uint32array";case"Float32Array":return"float32array";case"Float64Array":return"float64array"}if(function(t){return"function"==typeof t.throw&&"function"==typeof t.return&&"function"==typeof t.next}(t))return"generator";switch(e=i.call(t)){case"[object Object]":return"object";case"[object Map Iterator]":return"mapiterator";case"[object Set Iterator]":return"setiterator";case"[object String Iterator]":return"stringiterator";case"[object Array Iterator]":return"arrayiterator"}return e.slice(8,-1).toLowerCase().replace(/\s/g,"")};function o(t){return t.constructor?t.constructor.name:null}const s="@@__STRUCT__@@",l="@@__KIND__@@";function c(t){return!(!t||!t[s])}function u(t,e){return"function"==typeof t?t(e):t}var p=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var n=arguments[e];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(t[r]=n[r])}return t};class d{constructor(t,e,n){this.name=t,this.type=e,this.validate=n}}function h(t,e,n){if(c(t))return t[l];if(t instanceof d)return t;switch(a(t)){case"array":return t.length>1?w(t,e,n):v(t,e,n);case"function":return y(t,e,n);case"object":return m(t,e,n);case"string":{let r,i=!0;if(t.endsWith("?")&&(i=!1,t=t.slice(0,-1)),t.includes("|")){r=_(t.split(/\s*\|\s*/g),e,n)}else if(t.includes("&")){r=$(t.split(/\s*&\s*/g),e,n)}else r=b(t,e,n);return i||(r=g(r,void 0,n)),r}}throw new Error(`Invalid schema: ${t}`)}function f(t,e,n){if("array"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=t.map(t=>{try{return JSON.stringify(t)}catch(e){return String(t)}}).join(" | ");return new d("enum",r,(n=u(e))=>t.includes(n)?[void 0,n]:[{data:n,path:[],value:n,type:r}])}function y(t,e,n){if("function"!==a(t))throw new Error(`Invalid schema: ${t}`);return new d("function","<function>",(n=u(e),r)=>{const i=t(n,r);let o,s={path:[],reason:null};switch(a(i)){case"boolean":o=i;break;case"string":o=!1,s.reason=i;break;case"object":o=!1,s=p({},s,i);break;default:throw new Error(`Invalid result: ${i}`)}return o?[void 0,n]:[p({type:"<function>",value:n,data:n},s)]})}function v(t,e,n){if("array"!==a(t)||1!==t.length)throw new Error(`Invalid schema: ${t}`);const r=b("array",void 0,n),i=h(t[0],void 0,n),o=`[${i.type}]`;return new d("list",o,(t=u(e))=>{const[n,a]=r.validate(t);if(n)return n.type=o,[n];t=a;const s=[],l=[];for(let e=0;e<t.length;e++){const n=t[e],[r,a]=i.validate(n);r?(r.errors||[r]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,s.push(n)}):l[e]=a}if(s.length){const t=s[0];return t.errors=s,[t]}return[void 0,l]})}function m(t,e,n){if("object"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=b("object",void 0,n),i=[],o={};for(const a in t){i.push(a);const e=h(t[a],void 0,n);o[a]=e}const s=`{${i.join()}}`;return new d("object",s,(t=u(e))=>{const[n]=r.validate(t);if(n)return n.type=s,[n];const i=[],a={},l=Object.keys(t),c=Object.keys(o);if(new Set(l.concat(c)).forEach(n=>{let r=t[n];const s=o[n];if(void 0===r&&(r=u(e&&e[n],t)),!s){const e={data:t,path:[n],value:r};return void i.push(e)}const[l,c]=s.validate(r,t);l?(l.errors||[l]).forEach(e=>{e.path=[n].concat(e.path),e.data=t,i.push(e)}):(n in t||void 0!==c)&&(a[n]=c)}),i.length){const t=i[0];return t.errors=i,[t]}return[void 0,a]})}function g(t,e,n){return _([t,"undefined"],e,n)}function b(t,e,n){if("string"!==a(t))throw new Error(`Invalid schema: ${t}`);const{types:r}=n,i=r[t];if("function"!==a(i))throw new Error(`Invalid type: ${t}`);const o=y(i,e),s=t;return new d("scalar",s,t=>{const[e,n]=o.validate(t);return e?(e.type=s,[e]):[void 0,n]})}function w(t,e,n){if("array"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=t.map(t=>h(t,void 0,n)),i=b("array",void 0,n),o=`[${r.map(t=>t.type).join()}]`;return new d("tuple",o,(t=u(e))=>{const[n]=i.validate(t);if(n)return n.type=o,[n];const a=[],s=[],l=Math.max(t.length,r.length);for(let e=0;e<l;e++){const n=r[e],i=t[e];if(!n){const n={data:t,path:[e],value:i};s.push(n);continue}const[o,l]=n.validate(i);o?(o.errors||[o]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,s.push(n)}):a[e]=l}if(s.length){const t=s[0];return t.errors=s,[t]}return[void 0,a]})}function _(t,e,n){if("array"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=t.map(t=>h(t,void 0,n)),i=r.map(t=>t.type).join(" | ");return new d("union",i,(t=u(e))=>{const n=[];for(const e of r){const[r,i]=e.validate(t);if(!r)return[void 0,i];n.push(r)}return n[0].type=i,n})}function $(t,e,n){if("array"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=t.map(t=>h(t,void 0,n)),i=r.map(t=>t.type).join(" & ");return new d("intersection",i,(t=u(e))=>{let n=t;for(const e of r){const[t,r]=e.validate(n);if(t)return t.type=i,[t];n=r}return[void 0,n]})}const E={any:h,dict:function(t,e,n){if("array"!==a(t)||2!==t.length)throw new Error(`Invalid schema: ${t}`);const r=b("object",void 0,n),i=h(t[0],void 0,n),o=h(t[1],void 0,n),s=`dict<${i.type},${o.type}>`;return new d("dict",s,t=>{const n=u(e);t=n?p({},n,t):t;const[a]=r.validate(t);if(a)return a.type=s,[a];const l={},c=[];for(let e in t){const n=t[e],[r,a]=i.validate(e);if(r){(r.errors||[r]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,c.push(n)});continue}e=a;const[s,u]=o.validate(n);s?(s.errors||[s]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,c.push(n)}):l[e]=u}if(c.length){const t=c[0];return t.errors=c,[t]}return[void 0,l]})},enum:f,enums:function(t,e,n){return v([f(t,void 0)],e,n)},function:y,instance:function(t,e,n){const r=`instance<${t.name}>`;return new d("instance",r,(n=u(e))=>n instanceof t?[void 0,n]:[{data:n,path:[],value:n,type:r}])},interface:function(t,e,n){if("object"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=[],i={};for(const a in t){r.push(a);const e=h(t[a],void 0,n);i[a]=e}const o=`{${r.join()}}`;return new d("interface",o,t=>{const n=u(e);t=n?p({},n,t):t;const r=[],a=t;for(const o in i){let n=t[o];const s=i[o];void 0===n&&(n=u(e&&e[o],t));const[l,c]=s.validate(n,t);l?(l.errors||[l]).forEach(e=>{e.path=[o].concat(e.path),e.data=t,r.push(e)}):(o in t||void 0!==c)&&(a[o]=c)}if(r.length){const t=r[0];return t.errors=r,[t]}return[void 0,a]})},lazy:function(t,e,n){if("function"!==a(t))throw new Error(`Invalid schema: ${t}`);let r,i;return r=new d("lazy","lazy...",e=>(i=t(),r.name=i.kind,r.type=i.type,r.validate=i.validate,r.validate(e)))},list:v,literal:function(t,e,n){const r=`literal: ${JSON.stringify(t)}`;return new d("literal",r,(n=u(e))=>n===t?[void 0,n]:[{data:n,path:[],value:n,type:r}])},object:m,optional:g,partial:function(t,e,n){if("object"!==a(t))throw new Error(`Invalid schema: ${t}`);const r=b("object",void 0,n),i=[],o={};for(const a in t){i.push(a);const e=h(t[a],void 0,n);o[a]=e}const s=`{${i.join()},...}`;return new d("partial",s,(t=u(e))=>{const[n]=r.validate(t);if(n)return n.type=s,[n];const i=[],a={};for(const r in o){let n=t[r];const s=o[r];void 0===n&&(n=u(e&&e[r],t));const[l,c]=s.validate(n,t);l?(l.errors||[l]).forEach(e=>{e.path=[r].concat(e.path),e.data=t,i.push(e)}):(r in t||void 0!==c)&&(a[r]=c)}if(i.length){const t=i[0];return t.errors=i,[t]}return[void 0,a]})},scalar:b,tuple:w,union:_,intersection:$,dynamic:function(t,e,n){if("function"!==a(t))throw new Error(`Invalid schema: ${t}`);return new d("dynamic","dynamic...",(n=u(e),r)=>{const i=t(n,r);if("function"!==a(i))throw new Error(`Invalid schema: ${i}`);const[o,s]=i.validate(n);return o?[o]:[void 0,s]})}},k={any:t=>void 0!==t};function T(t={}){const e=p({},k,t.types||{});function n(t,n,i={}){c(t)&&(t=t.schema);const a=E.any(t,n,p({},i,{types:e}));function o(t){if(this instanceof o)throw new Error("Invalid `new` keyword!");return o.assert(t)}return Object.defineProperty(o,s,{value:!0}),Object.defineProperty(o,l,{value:a}),o.kind=a.name,o.type=a.type,o.schema=t,o.defaults=n,o.options=i,o.assert=(t=>{const[e,n]=a.validate(t);if(e)throw new r(e);return n}),o.test=(t=>{const[e]=a.validate(t);return!e}),o.validate=(t=>{const[e,n]=a.validate(t);return e?[new r(e)]:[void 0,n]}),o}return Object.keys(E).forEach(t=>{const r=E[t];n[t]=((t,i,a)=>{return n(r(t,i,p({},a,{types:e})),i,a)})}),n}["arguments","array","boolean","buffer","error","float32array","float64array","function","generatorfunction","int16array","int32array","int8array","map","null","number","object","promise","regexp","set","string","symbol","uint16array","uint32array","uint8array","uint8clampedarray","undefined","weakmap","weakset"].forEach(t=>{k[t]=(e=>a(e)===t)}),k.date=(t=>"date"===a(t)&&!isNaN(t));T()},64:function(t,e,n){"use strict";n.d(e,"a",function(){return r});n(3);const r={properties:{name:{type:String},value:{notify:!0,type:String},required:{type:Boolean,value:!1}},attached:function(){},detached:function(){}}},65:function(t,e,n){"use strict";n.d(e,"a",function(){return a});n(3);var r=n(53);let i=null;const a={properties:{validator:{type:String},invalid:{notify:!0,reflectToAttribute:!0,type:Boolean,value:!1,observer:"_invalidChanged"}},registered:function(){i=new r.a({type:"validator"})},_invalidChanged:function(){this.invalid?this.setAttribute("aria-invalid","true"):this.removeAttribute("aria-invalid")},get _validator(){return i&&i.byKey(this.validator)},hasValidator:function(){return null!=this._validator},validate:function(t){return void 0===t&&void 0!==this.value?this.invalid=!this._getValidity(this.value):this.invalid=!this._getValidity(t),!this.invalid},_getValidity:function(t){return!this.hasValidator()||this._validator.validate(t)}}},76:function(t,e,n){"use strict";n(3),n(124),n(125),n(126),n(127);var r=n(64),i=(n(45),n(5)),a=n(4),o=n(105);Object(i.a)({is:"paper-input",_template:a.a`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id$="[[_inputId]]" maxlength$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" disabled$="[[disabled]]" title$="[[title]]" type$="[[type]]" pattern$="[[pattern]]" required$="[[required]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" min$="[[min]]" max$="[[max]]" step$="[[step]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" list$="[[list]]" size$="[[size]]" autocapitalize$="[[autocapitalize]]" autocorrect$="[[autocorrect]]" on-change="_onChange" tabindex$="[[tabIndex]]" autosave$="[[autosave]]" results$="[[results]]" accept$="[[accept]]" multiple$="[[multiple]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[o.a,r.a],properties:{value:{type:String}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){this.$.nativeInput||(this.$.nativeInput=this.$$("input")),this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)&&(this.alwaysFloatLabel=!0),this.inputElement.bindValue&&this.$.container._handleValueAndAutoValidate(this.inputElement)}})}}]);
//# sourceMappingURL=chunk.d5ce454304253c0cef67.js.map
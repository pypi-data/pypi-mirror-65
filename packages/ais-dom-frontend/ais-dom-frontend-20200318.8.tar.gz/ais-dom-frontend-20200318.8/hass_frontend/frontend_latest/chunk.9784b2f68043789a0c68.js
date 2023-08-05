/*! For license information please see chunk.9784b2f68043789a0c68.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[170],{221:function(t,e,n){"use strict";n.d(e,"a",function(){return C});class o extends TypeError{static format(t){const{type:e,path:n,value:o}=t;return`Expected a value of type \`${e}\`${n.length?` for \`${n.join(".")}\``:""} but received \`${JSON.stringify(o)}\`.`}constructor(t){super(o.format(t));const{data:e,path:n,value:r,reason:i,type:a,errors:s=[]}=t;this.data=e,this.path=n,this.value=r,this.reason=i,this.type=a,this.errors=s,s.length||s.push(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=(new Error).stack}}var r=Object.prototype.toString,i=function(t){if(void 0===t)return"undefined";if(null===t)return"null";var e=typeof t;if("boolean"===e)return"boolean";if("string"===e)return"string";if("number"===e)return"number";if("symbol"===e)return"symbol";if("function"===e)return"GeneratorFunction"===a(t)?"generatorfunction":"function";if(function(t){return Array.isArray?Array.isArray(t):t instanceof Array}(t))return"array";if(function(t){if(t.constructor&&"function"==typeof t.constructor.isBuffer)return t.constructor.isBuffer(t);return!1}(t))return"buffer";if(function(t){try{if("number"==typeof t.length&&"function"==typeof t.callee)return!0}catch(e){if(-1!==e.message.indexOf("callee"))return!0}return!1}(t))return"arguments";if(function(t){return t instanceof Date||"function"==typeof t.toDateString&&"function"==typeof t.getDate&&"function"==typeof t.setDate}(t))return"date";if(function(t){return t instanceof Error||"string"==typeof t.message&&t.constructor&&"number"==typeof t.constructor.stackTraceLimit}(t))return"error";if(function(t){return t instanceof RegExp||"string"==typeof t.flags&&"boolean"==typeof t.ignoreCase&&"boolean"==typeof t.multiline&&"boolean"==typeof t.global}(t))return"regexp";switch(a(t)){case"Symbol":return"symbol";case"Promise":return"promise";case"WeakMap":return"weakmap";case"WeakSet":return"weakset";case"Map":return"map";case"Set":return"set";case"Int8Array":return"int8array";case"Uint8Array":return"uint8array";case"Uint8ClampedArray":return"uint8clampedarray";case"Int16Array":return"int16array";case"Uint16Array":return"uint16array";case"Int32Array":return"int32array";case"Uint32Array":return"uint32array";case"Float32Array":return"float32array";case"Float64Array":return"float64array"}if(function(t){return"function"==typeof t.throw&&"function"==typeof t.return&&"function"==typeof t.next}(t))return"generator";switch(e=r.call(t)){case"[object Object]":return"object";case"[object Map Iterator]":return"mapiterator";case"[object Set Iterator]":return"setiterator";case"[object String Iterator]":return"stringiterator";case"[object Array Iterator]":return"arrayiterator"}return e.slice(8,-1).toLowerCase().replace(/\s/g,"")};function a(t){return t.constructor?t.constructor.name:null}const s="@@__STRUCT__@@",c="@@__KIND__@@";function l(t){return!(!t||!t[s])}function u(t,e){return"function"==typeof t?t(e):t}var h=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var n=arguments[e];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(t[o]=n[o])}return t};class p{constructor(t,e,n){this.name=t,this.type=e,this.validate=n}}function d(t,e,n){if(l(t))return t[c];if(t instanceof p)return t;switch(i(t)){case"array":return t.length>1?m(t,e,n):y(t,e,n);case"function":return v(t,e,n);case"object":return b(t,e,n);case"string":{let o,r=!0;if(t.endsWith("?")&&(r=!1,t=t.slice(0,-1)),t.includes("|")){o=w(t.split(/\s*\|\s*/g),e,n)}else if(t.includes("&")){o=k(t.split(/\s*&\s*/g),e,n)}else o=g(t,e,n);return r||(o=_(o,void 0,n)),o}}throw new Error(`Invalid schema: ${t}`)}function f(t,e,n){if("array"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=t.map(t=>{try{return JSON.stringify(t)}catch(e){return String(t)}}).join(" | ");return new p("enum",o,(n=u(e))=>t.includes(n)?[void 0,n]:[{data:n,path:[],value:n,type:o}])}function v(t,e,n){if("function"!==i(t))throw new Error(`Invalid schema: ${t}`);return new p("function","<function>",(n=u(e),o)=>{const r=t(n,o);let a,s={path:[],reason:null};switch(i(r)){case"boolean":a=r;break;case"string":a=!1,s.reason=r;break;case"object":a=!1,s=h({},s,r);break;default:throw new Error(`Invalid result: ${r}`)}return a?[void 0,n]:[h({type:"<function>",value:n,data:n},s)]})}function y(t,e,n){if("array"!==i(t)||1!==t.length)throw new Error(`Invalid schema: ${t}`);const o=g("array",void 0,n),r=d(t[0],void 0,n),a=`[${r.type}]`;return new p("list",a,(t=u(e))=>{const[n,i]=o.validate(t);if(n)return n.type=a,[n];t=i;const s=[],c=[];for(let e=0;e<t.length;e++){const n=t[e],[o,i]=r.validate(n);o?(o.errors||[o]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,s.push(n)}):c[e]=i}if(s.length){const t=s[0];return t.errors=s,[t]}return[void 0,c]})}function b(t,e,n){if("object"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=g("object",void 0,n),r=[],a={};for(const i in t){r.push(i);const e=d(t[i],void 0,n);a[i]=e}const s=`{${r.join()}}`;return new p("object",s,(t=u(e))=>{const[n]=o.validate(t);if(n)return n.type=s,[n];const r=[],i={},c=Object.keys(t),l=Object.keys(a);if(new Set(c.concat(l)).forEach(n=>{let o=t[n];const s=a[n];if(void 0===o&&(o=u(e&&e[n],t)),!s){const e={data:t,path:[n],value:o};return void r.push(e)}const[c,l]=s.validate(o,t);c?(c.errors||[c]).forEach(e=>{e.path=[n].concat(e.path),e.data=t,r.push(e)}):(n in t||void 0!==l)&&(i[n]=l)}),r.length){const t=r[0];return t.errors=r,[t]}return[void 0,i]})}function _(t,e,n){return w([t,"undefined"],e,n)}function g(t,e,n){if("string"!==i(t))throw new Error(`Invalid schema: ${t}`);const{types:o}=n,r=o[t];if("function"!==i(r))throw new Error(`Invalid type: ${t}`);const a=v(r,e),s=t;return new p("scalar",s,t=>{const[e,n]=a.validate(t);return e?(e.type=s,[e]):[void 0,n]})}function m(t,e,n){if("array"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=t.map(t=>d(t,void 0,n)),r=g("array",void 0,n),a=`[${o.map(t=>t.type).join()}]`;return new p("tuple",a,(t=u(e))=>{const[n]=r.validate(t);if(n)return n.type=a,[n];const i=[],s=[],c=Math.max(t.length,o.length);for(let e=0;e<c;e++){const n=o[e],r=t[e];if(!n){const n={data:t,path:[e],value:r};s.push(n);continue}const[a,c]=n.validate(r);a?(a.errors||[a]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,s.push(n)}):i[e]=c}if(s.length){const t=s[0];return t.errors=s,[t]}return[void 0,i]})}function w(t,e,n){if("array"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=t.map(t=>d(t,void 0,n)),r=o.map(t=>t.type).join(" | ");return new p("union",r,(t=u(e))=>{const n=[];for(const e of o){const[o,r]=e.validate(t);if(!o)return[void 0,r];n.push(o)}return n[0].type=r,n})}function k(t,e,n){if("array"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=t.map(t=>d(t,void 0,n)),r=o.map(t=>t.type).join(" & ");return new p("intersection",r,(t=u(e))=>{let n=t;for(const e of o){const[t,o]=e.validate(n);if(t)return t.type=r,[t];n=o}return[void 0,n]})}const B={any:d,dict:function(t,e,n){if("array"!==i(t)||2!==t.length)throw new Error(`Invalid schema: ${t}`);const o=g("object",void 0,n),r=d(t[0],void 0,n),a=d(t[1],void 0,n),s=`dict<${r.type},${a.type}>`;return new p("dict",s,t=>{const n=u(e);t=n?h({},n,t):t;const[i]=o.validate(t);if(i)return i.type=s,[i];const c={},l=[];for(let e in t){const n=t[e],[o,i]=r.validate(e);if(o){(o.errors||[o]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,l.push(n)});continue}e=i;const[s,u]=a.validate(n);s?(s.errors||[s]).forEach(n=>{n.path=[e].concat(n.path),n.data=t,l.push(n)}):c[e]=u}if(l.length){const t=l[0];return t.errors=l,[t]}return[void 0,c]})},enum:f,enums:function(t,e,n){return y([f(t,void 0)],e,n)},function:v,instance:function(t,e,n){const o=`instance<${t.name}>`;return new p("instance",o,(n=u(e))=>n instanceof t?[void 0,n]:[{data:n,path:[],value:n,type:o}])},interface:function(t,e,n){if("object"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=[],r={};for(const i in t){o.push(i);const e=d(t[i],void 0,n);r[i]=e}const a=`{${o.join()}}`;return new p("interface",a,t=>{const n=u(e);t=n?h({},n,t):t;const o=[],i=t;for(const a in r){let n=t[a];const s=r[a];void 0===n&&(n=u(e&&e[a],t));const[c,l]=s.validate(n,t);c?(c.errors||[c]).forEach(e=>{e.path=[a].concat(e.path),e.data=t,o.push(e)}):(a in t||void 0!==l)&&(i[a]=l)}if(o.length){const t=o[0];return t.errors=o,[t]}return[void 0,i]})},lazy:function(t,e,n){if("function"!==i(t))throw new Error(`Invalid schema: ${t}`);let o,r;return o=new p("lazy","lazy...",e=>(r=t(),o.name=r.kind,o.type=r.type,o.validate=r.validate,o.validate(e)))},list:y,literal:function(t,e,n){const o=`literal: ${JSON.stringify(t)}`;return new p("literal",o,(n=u(e))=>n===t?[void 0,n]:[{data:n,path:[],value:n,type:o}])},object:b,optional:_,partial:function(t,e,n){if("object"!==i(t))throw new Error(`Invalid schema: ${t}`);const o=g("object",void 0,n),r=[],a={};for(const i in t){r.push(i);const e=d(t[i],void 0,n);a[i]=e}const s=`{${r.join()},...}`;return new p("partial",s,(t=u(e))=>{const[n]=o.validate(t);if(n)return n.type=s,[n];const r=[],i={};for(const o in a){let n=t[o];const s=a[o];void 0===n&&(n=u(e&&e[o],t));const[c,l]=s.validate(n,t);c?(c.errors||[c]).forEach(e=>{e.path=[o].concat(e.path),e.data=t,r.push(e)}):(o in t||void 0!==l)&&(i[o]=l)}if(r.length){const t=r[0];return t.errors=r,[t]}return[void 0,i]})},scalar:g,tuple:m,union:w,intersection:k,dynamic:function(t,e,n){if("function"!==i(t))throw new Error(`Invalid schema: ${t}`);return new p("dynamic","dynamic...",(n=u(e),o)=>{const r=t(n,o);if("function"!==i(r))throw new Error(`Invalid schema: ${r}`);const[a,s]=r.validate(n);return a?[a]:[void 0,s]})}},A={any:t=>void 0!==t};function C(t={}){const e=h({},A,t.types||{});function n(t,n,r={}){l(t)&&(t=t.schema);const i=B.any(t,n,h({},r,{types:e}));function a(t){if(this instanceof a)throw new Error("Invalid `new` keyword!");return a.assert(t)}return Object.defineProperty(a,s,{value:!0}),Object.defineProperty(a,c,{value:i}),a.kind=i.name,a.type=i.type,a.schema=t,a.defaults=n,a.options=r,a.assert=(t=>{const[e,n]=i.validate(t);if(e)throw new o(e);return n}),a.test=(t=>{const[e]=i.validate(t);return!e}),a.validate=(t=>{const[e,n]=i.validate(t);return e?[new o(e)]:[void 0,n]}),a}return Object.keys(B).forEach(t=>{const o=B[t];n[t]=((t,r,i)=>{return n(o(t,r,h({},i,{types:e})),r,i)})}),n}["arguments","array","boolean","buffer","error","float32array","float64array","function","generatorfunction","int16array","int32array","int8array","map","null","number","object","promise","regexp","set","string","symbol","uint16array","uint32array","uint8array","uint8clampedarray","undefined","weakmap","weakset"].forEach(t=>{A[t]=(e=>i(e)===t)}),A.date=(t=>"date"===i(t)&&!isNaN(t));C()},291:function(t,e,n){"use strict";n.d(e,"b",function(){return r}),n.d(e,"a",function(){return i});n(3);var o=n(143);const r={hostAttributes:{role:"menubar"},keyBindings:{left:"_onLeftKey",right:"_onRightKey"},_onUpKey:function(t){this.focusedItem.click(),t.detail.keyboardEvent.preventDefault()},_onDownKey:function(t){this.focusedItem.click(),t.detail.keyboardEvent.preventDefault()},get _isRTL(){return"rtl"===window.getComputedStyle(this).direction},_onLeftKey:function(t){this._isRTL?this._focusNext():this._focusPrevious(),t.detail.keyboardEvent.preventDefault()},_onRightKey:function(t){this._isRTL?this._focusPrevious():this._focusNext(),t.detail.keyboardEvent.preventDefault()},_onKeydown:function(t){this.keyboardEventMatchesKeys(t,"up down left right esc")||this._focusWithKeyboardEvent(t)}},i=[o.a,r]},298:function(t,e,n){"use strict";n(3),n(51);var o=n(60),r=n(38),i=n(73),a=n(5),s=n(1),c=n(4);Object(a.a)({_template:c.a`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center;
        @apply --layout-center-justified;
        @apply --layout-flex-auto;

        position: relative;
        padding: 0 12px;
        overflow: hidden;
        cursor: pointer;
        vertical-align: middle;

        @apply --paper-font-common-base;
        @apply --paper-tab;
      }

      :host(:focus) {
        outline: none;
      }

      :host([link]) {
        padding: 0;
      }

      .tab-content {
        height: 100%;
        transform: translateZ(0);
          -webkit-transform: translateZ(0);
        transition: opacity 0.1s cubic-bezier(0.4, 0.0, 1, 1);
        @apply --layout-horizontal;
        @apply --layout-center-center;
        @apply --layout-flex-auto;
        @apply --paper-tab-content;
      }

      :host(:not(.iron-selected)) > .tab-content {
        opacity: 0.8;

        @apply --paper-tab-content-unselected;
      }

      :host(:focus) .tab-content {
        opacity: 1;
        font-weight: 700;

        @apply --paper-tab-content-focused;
      }

      paper-ripple {
        color: var(--paper-tab-ink, var(--paper-yellow-a100));
      }

      .tab-content > ::slotted(a) {
        @apply --layout-flex-auto;

        height: 100%;
      }
    </style>

    <div class="tab-content">
      <slot></slot>
    </div>
`,is:"paper-tab",behaviors:[r.a,o.a,i.a],properties:{link:{type:Boolean,value:!1,reflectToAttribute:!0}},hostAttributes:{role:"tab"},listeners:{down:"_updateNoink",tap:"_onTap"},attached:function(){this._updateNoink()},get _parentNoink(){var t=Object(s.a)(this).parentNode;return!!t&&!!t.noink},_updateNoink:function(){this.noink=!!this.noink||!!this._parentNoink},_onTap:function(t){if(this.link){var e=this.queryEffectiveChildren("a");if(!e)return;if(t.target===e)return;e.click()}}})},327:function(t,e,n){"use strict";n(3),n(51),n(120),n(119),n(72),n(95);var o=n(4);const r=o.a`<iron-iconset-svg name="paper-tabs" size="24">
<svg><defs>
<g id="chevron-left"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path></g>
<g id="chevron-right"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path></g>
</defs></svg>
</iron-iconset-svg>`;document.head.appendChild(r.content);n(298);var i=n(143),a=n(291),s=n(109),c=n(5),l=n(1);Object(c.a)({_template:o.a`
    <style>
      :host {
        @apply --layout;
        @apply --layout-center;

        height: 48px;
        font-size: 14px;
        font-weight: 500;
        overflow: hidden;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;

        /* NOTE: Both values are needed, since some phones require the value to be \`transparent\`. */
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-tap-highlight-color: transparent;

        @apply --paper-tabs;
      }

      :host(:dir(rtl)) {
        @apply --layout-horizontal-reverse;
      }

      #tabsContainer {
        position: relative;
        height: 100%;
        white-space: nowrap;
        overflow: hidden;
        @apply --layout-flex-auto;
        @apply --paper-tabs-container;
      }

      #tabsContent {
        height: 100%;
        -moz-flex-basis: auto;
        -ms-flex-basis: auto;
        flex-basis: auto;
        @apply --paper-tabs-content;
      }

      #tabsContent.scrollable {
        position: absolute;
        white-space: nowrap;
      }

      #tabsContent:not(.scrollable),
      #tabsContent.scrollable.fit-container {
        @apply --layout-horizontal;
      }

      #tabsContent.scrollable.fit-container {
        min-width: 100%;
      }

      #tabsContent.scrollable.fit-container > ::slotted(*) {
        /* IE - prevent tabs from compressing when they should scroll. */
        -ms-flex: 1 0 auto;
        -webkit-flex: 1 0 auto;
        flex: 1 0 auto;
      }

      .hidden {
        display: none;
      }

      .not-visible {
        opacity: 0;
        cursor: default;
      }

      paper-icon-button {
        width: 48px;
        height: 48px;
        padding: 12px;
        margin: 0 4px;
      }

      #selectionBar {
        position: absolute;
        height: 0;
        bottom: 0;
        left: 0;
        right: 0;
        border-bottom: 2px solid var(--paper-tabs-selection-bar-color, var(--paper-yellow-a100));
          -webkit-transform: scale(0);
        transform: scale(0);
          -webkit-transform-origin: left center;
        transform-origin: left center;
          transition: -webkit-transform;
        transition: transform;

        @apply --paper-tabs-selection-bar;
      }

      #selectionBar.align-bottom {
        top: 0;
        bottom: auto;
      }

      #selectionBar.expand {
        transition-duration: 0.15s;
        transition-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
      }

      #selectionBar.contract {
        transition-duration: 0.18s;
        transition-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
      }

      #tabsContent > ::slotted(:not(#selectionBar)) {
        height: 100%;
      }
    </style>

    <paper-icon-button icon="paper-tabs:chevron-left" class$="[[_computeScrollButtonClass(_leftHidden, scrollable, hideScrollButtons)]]" on-up="_onScrollButtonUp" on-down="_onLeftScrollButtonDown" tabindex="-1"></paper-icon-button>

    <div id="tabsContainer" on-track="_scroll" on-down="_down">
      <div id="tabsContent" class$="[[_computeTabsContentClass(scrollable, fitContainer)]]">
        <div id="selectionBar" class$="[[_computeSelectionBarClass(noBar, alignBottom)]]" on-transitionend="_onBarTransitionEnd"></div>
        <slot></slot>
      </div>
    </div>

    <paper-icon-button icon="paper-tabs:chevron-right" class$="[[_computeScrollButtonClass(_rightHidden, scrollable, hideScrollButtons)]]" on-up="_onScrollButtonUp" on-down="_onRightScrollButtonDown" tabindex="-1"></paper-icon-button>
`,is:"paper-tabs",behaviors:[s.a,a.a],properties:{noink:{type:Boolean,value:!1,observer:"_noinkChanged"},noBar:{type:Boolean,value:!1},noSlide:{type:Boolean,value:!1},scrollable:{type:Boolean,value:!1},fitContainer:{type:Boolean,value:!1},disableDrag:{type:Boolean,value:!1},hideScrollButtons:{type:Boolean,value:!1},alignBottom:{type:Boolean,value:!1},selectable:{type:String,value:"paper-tab"},autoselect:{type:Boolean,value:!1},autoselectDelay:{type:Number,value:0},_step:{type:Number,value:10},_holdDelay:{type:Number,value:1},_leftHidden:{type:Boolean,value:!1},_rightHidden:{type:Boolean,value:!1},_previousTab:{type:Object}},hostAttributes:{role:"tablist"},listeners:{"iron-resize":"_onTabSizingChanged","iron-items-changed":"_onTabSizingChanged","iron-select":"_onIronSelect","iron-deselect":"_onIronDeselect"},keyBindings:{"left:keyup right:keyup":"_onArrowKeyup"},created:function(){this._holdJob=null,this._pendingActivationItem=void 0,this._pendingActivationTimeout=void 0,this._bindDelayedActivationHandler=this._delayedActivationHandler.bind(this),this.addEventListener("blur",this._onBlurCapture.bind(this),!0)},ready:function(){this.setScrollDirection("y",this.$.tabsContainer)},detached:function(){this._cancelPendingActivation()},_noinkChanged:function(t){Object(l.a)(this).querySelectorAll("paper-tab").forEach(t?this._setNoinkAttribute:this._removeNoinkAttribute)},_setNoinkAttribute:function(t){t.setAttribute("noink","")},_removeNoinkAttribute:function(t){t.removeAttribute("noink")},_computeScrollButtonClass:function(t,e,n){return!e||n?"hidden":t?"not-visible":""},_computeTabsContentClass:function(t,e){return t?"scrollable"+(e?" fit-container":""):" fit-container"},_computeSelectionBarClass:function(t,e){return t?"hidden":e?"align-bottom":""},_onTabSizingChanged:function(){this.debounce("_onTabSizingChanged",function(){this._scroll(),this._tabChanged(this.selectedItem)},10)},_onIronSelect:function(t){this._tabChanged(t.detail.item,this._previousTab),this._previousTab=t.detail.item,this.cancelDebouncer("tab-changed")},_onIronDeselect:function(t){this.debounce("tab-changed",function(){this._tabChanged(null,this._previousTab),this._previousTab=null},1)},_activateHandler:function(){this._cancelPendingActivation(),i.b._activateHandler.apply(this,arguments)},_scheduleActivation:function(t,e){this._pendingActivationItem=t,this._pendingActivationTimeout=this.async(this._bindDelayedActivationHandler,e)},_delayedActivationHandler:function(){var t=this._pendingActivationItem;this._pendingActivationItem=void 0,this._pendingActivationTimeout=void 0,t.fire(this.activateEvent,null,{bubbles:!0,cancelable:!0})},_cancelPendingActivation:function(){void 0!==this._pendingActivationTimeout&&(this.cancelAsync(this._pendingActivationTimeout),this._pendingActivationItem=void 0,this._pendingActivationTimeout=void 0)},_onArrowKeyup:function(t){this.autoselect&&this._scheduleActivation(this.focusedItem,this.autoselectDelay)},_onBlurCapture:function(t){t.target===this._pendingActivationItem&&this._cancelPendingActivation()},get _tabContainerScrollSize(){return Math.max(0,this.$.tabsContainer.scrollWidth-this.$.tabsContainer.offsetWidth)},_scroll:function(t,e){if(this.scrollable){var n=e&&-e.ddx||0;this._affectScroll(n)}},_down:function(t){this.async(function(){this._defaultFocusAsync&&(this.cancelAsync(this._defaultFocusAsync),this._defaultFocusAsync=null)},1)},_affectScroll:function(t){this.$.tabsContainer.scrollLeft+=t;var e=this.$.tabsContainer.scrollLeft;this._leftHidden=0===e,this._rightHidden=e===this._tabContainerScrollSize},_onLeftScrollButtonDown:function(){this._scrollToLeft(),this._holdJob=setInterval(this._scrollToLeft.bind(this),this._holdDelay)},_onRightScrollButtonDown:function(){this._scrollToRight(),this._holdJob=setInterval(this._scrollToRight.bind(this),this._holdDelay)},_onScrollButtonUp:function(){clearInterval(this._holdJob),this._holdJob=null},_scrollToLeft:function(){this._affectScroll(-this._step)},_scrollToRight:function(){this._affectScroll(this._step)},_tabChanged:function(t,e){if(!t)return this.$.selectionBar.classList.remove("expand"),this.$.selectionBar.classList.remove("contract"),void this._positionBar(0,0);var n=this.$.tabsContent.getBoundingClientRect(),o=n.width,r=t.getBoundingClientRect(),i=r.left-n.left;if(this._pos={width:this._calcPercent(r.width,o),left:this._calcPercent(i,o)},this.noSlide||null==e)return this.$.selectionBar.classList.remove("expand"),this.$.selectionBar.classList.remove("contract"),void this._positionBar(this._pos.width,this._pos.left);var a=e.getBoundingClientRect(),s=this.items.indexOf(e),c=this.items.indexOf(t);this.$.selectionBar.classList.add("expand");var l=s<c;this._isRTL&&(l=!l),l?this._positionBar(this._calcPercent(r.left+r.width-a.left,o)-5,this._left):this._positionBar(this._calcPercent(a.left+a.width-r.left,o)-5,this._calcPercent(i,o)+5),this.scrollable&&this._scrollToSelectedIfNeeded(r.width,i)},_scrollToSelectedIfNeeded:function(t,e){var n=e-this.$.tabsContainer.scrollLeft;n<0?this.$.tabsContainer.scrollLeft+=n:(n+=t-this.$.tabsContainer.offsetWidth)>0&&(this.$.tabsContainer.scrollLeft+=n)},_calcPercent:function(t,e){return 100*t/e},_positionBar:function(t,e){t=t||0,e=e||0,this._width=t,this._left=e,this.transform("translateX("+e+"%) scaleX("+t/100+")",this.$.selectionBar)},_onBarTransitionEnd:function(t){var e=this.$.selectionBar.classList;e.contains("expand")?(e.remove("expand"),e.add("contract"),this._positionBar(this._pos.width,this._pos.left)):e.contains("contract")&&e.remove("contract")}})}}]);
//# sourceMappingURL=chunk.9784b2f68043789a0c68.js.map
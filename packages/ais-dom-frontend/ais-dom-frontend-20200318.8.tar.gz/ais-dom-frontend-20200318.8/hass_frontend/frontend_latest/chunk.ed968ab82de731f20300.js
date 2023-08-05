/*! For license information please see chunk.ed968ab82de731f20300.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[212],{137:function(e,t,a){"use strict";a(3),a(47);var r=a(138),i=a(61),c=a(5),o=a(4),n=a(66);const l=o.a`<style>
  :host {
    display: inline-block;
    white-space: nowrap;
    cursor: pointer;
    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);
    /* -1px is a sentinel for the default and is replaced in \`attached\`. */
    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);
    @apply --paper-font-common-base;
    line-height: 0;
    -webkit-tap-highlight-color: transparent;
  }

  :host([hidden]) {
    display: none !important;
  }

  :host(:focus) {
    outline: none;
  }

  .hidden {
    display: none;
  }

  #checkboxContainer {
    display: inline-block;
    position: relative;
    width: var(--calculated-paper-checkbox-size);
    height: var(--calculated-paper-checkbox-size);
    min-width: var(--calculated-paper-checkbox-size);
    margin: var(--paper-checkbox-margin, initial);
    vertical-align: var(--paper-checkbox-vertical-align, middle);
    background-color: var(--paper-checkbox-unchecked-background-color, transparent);
  }

  #ink {
    position: absolute;

    /* Center the ripple in the checkbox by negative offsetting it by
     * (inkWidth - rippleWidth) / 2 */
    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    width: var(--calculated-paper-checkbox-ink-size);
    height: var(--calculated-paper-checkbox-ink-size);
    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
  }

  #ink:dir(rtl) {
    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: auto;
  }

  #ink[checked] {
    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));
  }

  #checkbox {
    position: relative;
    box-sizing: border-box;
    height: 100%;
    border: solid 2px;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    border-radius: 2px;
    pointer-events: none;
    -webkit-transition: background-color 140ms, border-color 140ms;
    transition: background-color 140ms, border-color 140ms;

    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);
    transition-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  /* checkbox checked animations */
  #checkbox.checked #checkmark {
    -webkit-animation: checkmark-expand 140ms ease-out forwards;
    animation: checkmark-expand 140ms ease-out forwards;

    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);
    animation-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  @-webkit-keyframes checkmark-expand {
    0% {
      -webkit-transform: scale(0, 0) rotate(45deg);
    }
    100% {
      -webkit-transform: scale(1, 1) rotate(45deg);
    }
  }

  @keyframes checkmark-expand {
    0% {
      transform: scale(0, 0) rotate(45deg);
    }
    100% {
      transform: scale(1, 1) rotate(45deg);
    }
  }

  #checkbox.checked {
    background-color: var(--paper-checkbox-checked-color, var(--primary-color));
    border-color: var(--paper-checkbox-checked-color, var(--primary-color));
  }

  #checkmark {
    position: absolute;
    width: 36%;
    height: 70%;
    border-style: solid;
    border-top: none;
    border-left: none;
    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-color: var(--paper-checkbox-checkmark-color, white);
    -webkit-transform-origin: 97% 86%;
    transform-origin: 97% 86%;
    box-sizing: content-box; /* protect against page-level box-sizing */
  }

  #checkmark:dir(rtl) {
    -webkit-transform-origin: 50% 14%;
    transform-origin: 50% 14%;
  }

  /* label */
  #checkboxLabel {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    padding-left: var(--paper-checkbox-label-spacing, 8px);
    white-space: normal;
    line-height: normal;
    color: var(--paper-checkbox-label-color, var(--primary-text-color));
    @apply --paper-checkbox-label;
  }

  :host([checked]) #checkboxLabel {
    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));
    @apply --paper-checkbox-label-checked;
  }

  #checkboxLabel:dir(rtl) {
    padding-right: var(--paper-checkbox-label-spacing, 8px);
    padding-left: 0;
  }

  #checkboxLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #checkbox {
    opacity: 0.5;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
  }

  :host([disabled][checked]) #checkbox {
    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #checkboxLabel  {
    opacity: 0.65;
  }

  /* invalid state */
  #checkbox.invalid:not(.checked) {
    border-color: var(--paper-checkbox-error-color, var(--error-color));
  }
</style>

<div id="checkboxContainer">
  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">
    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>
  </div>
</div>

<div id="checkboxLabel"><slot></slot></div>`;l.setAttribute("strip-whitespace",""),Object(c.a)({_template:l,is:"paper-checkbox",behaviors:[r.a],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){Object(n.a)(this,function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",a=e.match(/[A-Za-z]+$/);null!==a&&(t=a[0]);var r=parseFloat(e),i=8/3*r;"px"===t&&(i=Math.floor(i))%2!=r%2&&i++,this.updateStyles({"--paper-checkbox-ink-size":i+t})}})},_computeCheckboxClass:function(e,t){var a="";return e&&(a+="checked "),t&&(a+="invalid"),a},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,i.b._createRipple.call(this)}})},138:function(e,t,a){"use strict";a(3);var r=a(64),i=a(65);const c={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},o=[r.a,i.a,c];var n=a(61),l=a(73);a.d(t,"a",function(){return d});const s={_checkedChanged:function(){c._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){l.a._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},d=[n.a,o,s]},64:function(e,t,a){"use strict";a.d(t,"a",function(){return r});a(3);const r={properties:{name:{type:String},value:{notify:!0,type:String},required:{type:Boolean,value:!1}},attached:function(){},detached:function(){}}},65:function(e,t,a){"use strict";a.d(t,"a",function(){return c});a(3);var r=a(53);let i=null;const c={properties:{validator:{type:String},invalid:{notify:!0,reflectToAttribute:!0,type:Boolean,value:!1,observer:"_invalidChanged"}},registered:function(){i=new r.a({type:"validator"})},_invalidChanged:function(){this.invalid?this.setAttribute("aria-invalid","true"):this.removeAttribute("aria-invalid")},get _validator(){return i&&i.byKey(this.validator)},hasValidator:function(){return null!=this._validator},validate:function(e){return void 0===e&&void 0!==this.value?this.invalid=!this._getValidity(this.value):this.invalid=!this._getValidity(e),!this.invalid},_getValidity:function(e){return!this.hasValidator()||this._validator.validate(e)}}},774:function(e,t,a){"use strict";a.d(t,"a",function(){return h});var r=a(9);const i=(e,t)=>{const a=e.startNode.parentNode,i=void 0===t?e.endNode:t.startNode,c=a.insertBefore(Object(r.e)(),i);a.insertBefore(Object(r.e)(),i);const o=new r.b(e.options);return o.insertAfterNode(c),o},c=(e,t)=>(e.setValue(t),e.commit(),e),o=(e,t,a)=>{const i=e.startNode.parentNode,c=a?a.startNode:e.endNode,o=t.endNode.nextSibling;o!==c&&Object(r.j)(i,t.startNode,o,c)},n=e=>{Object(r.i)(e.startNode.parentNode,e.startNode,e.endNode.nextSibling)},l=(e,t,a)=>{const r=new Map;for(let i=t;i<=a;i++)r.set(e[i],i);return r},s=new WeakMap,d=new WeakMap,h=Object(r.f)((e,t,a)=>{let h;return void 0===a?a=t:void 0!==t&&(h=t),t=>{if(!(t instanceof r.b))throw new Error("repeat can only be used in text bindings");const p=s.get(t)||[],b=d.get(t)||[],k=[],u=[],v=[];let x,f,g=0;for(const r of e)v[g]=h?h(r,g):g,u[g]=a(r,g),g++;let m=0,y=p.length-1,w=0,_=u.length-1;for(;m<=y&&w<=_;)if(null===p[m])m++;else if(null===p[y])y--;else if(b[m]===v[w])k[w]=c(p[m],u[w]),m++,w++;else if(b[y]===v[_])k[_]=c(p[y],u[_]),y--,_--;else if(b[m]===v[_])k[_]=c(p[m],u[_]),o(t,p[m],k[_+1]),m++,_--;else if(b[y]===v[w])k[w]=c(p[y],u[w]),o(t,p[y],p[m]),y--,w++;else if(void 0===x&&(x=l(v,w,_),f=l(b,m,y)),x.has(b[m]))if(x.has(b[y])){const e=f.get(v[w]),a=void 0!==e?p[e]:null;if(null===a){const e=i(t,p[m]);c(e,u[w]),k[w]=e}else k[w]=c(a,u[w]),o(t,a,p[m]),p[e]=null;w++}else n(p[y]),y--;else n(p[m]),m++;for(;w<=_;){const e=i(t,k[_+1]);c(e,u[w]),k[w++]=e}for(;m<=y;){const e=p[m++];null!==e&&n(e)}s.set(t,k),d.set(t,v)}})}}]);
//# sourceMappingURL=chunk.ed968ab82de731f20300.js.map
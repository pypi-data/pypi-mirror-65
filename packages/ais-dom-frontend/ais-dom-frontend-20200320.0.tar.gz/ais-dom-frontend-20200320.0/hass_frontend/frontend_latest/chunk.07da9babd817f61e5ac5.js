(self.webpackJsonp=self.webpackJsonp||[]).push([[83],{214:function(e,t,r){"use strict";var i=r(221);r.d(t,"a",function(){return n});const n=Object(i.a)({types:{"entity-id":function(e){return"string"!=typeof e?"entity id should be a string":!!e.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(e){return"string"!=typeof e?"icon should be a string":!!e.includes(":")||"icon should be in the format 'mdi:icon'"}}})},872:function(e,t,r){"use strict";r.r(t),r.d(t,"HuiStackCardEditor",function(){return h});var i=r(0),n=(r(327),r(214)),o=r(12);function s(e){var t,r=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function l(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}const p=Object(n.a)({type:"string",cards:["any"],title:"string?"});let h=function(e,t,r,i){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(i){t.forEach(function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)},this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var d=c.extras;if(d){for(var l=0;l<d.length;l++)this.addElementPlacement(d[l],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=f(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=l(e,"finisher"),i=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:i}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=l(e,"finisher"),i=this.toElementDescriptors(e.elements);return{elements:i,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var p=t(function(e){n.initializeInstanceElements(e,h.elements)},r),h=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}a(o,n)}else t.push(o)}return t}(p.d.map(s)),e);return n.initializeClassElements(p.F,h.elements),n.runClassFinishers(p.F,h.finishers)}([Object(i.d)("hui-stack-card-editor")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(i.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"lovelace",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_config",value:void 0},{kind:"field",decorators:[Object(i.g)()],key:"_selectedCard",value:()=>0},{kind:"method",key:"setConfig",value:function(e){this._config=p(e)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return i.f``;const e=this._selectedCard,t=this._config.cards.length;return i.f`
      <div class="card-config">
        <div class="toolbar">
          <paper-tabs
            .selected=${e}
            scrollable
            @iron-select=${this._handleSelectedCard}
          >
            ${this._config.cards.map((e,t)=>i.f`
                <paper-tab>
                  ${t+1}
                </paper-tab>
              `)}
          </paper-tabs>
          <paper-tabs
            id="add-card"
            .selected=${e===t?"0":void 0}
            @iron-select=${this._handleSelectedCard}
          >
            <paper-tab>
              <ha-icon icon="hass:plus"></ha-icon>
            </paper-tab>
          <paper-tabs>
        </div>

        <div id="editor">
          ${e<t?i.f`
                  <div id="card-options">
                    <paper-icon-button
                      id="move-before"
                      title="Move card before"
                      icon="hass:arrow-left"
                      ?disabled=${0===e}
                      @click=${this._handleMove}
                    ></paper-icon-button>

                    <paper-icon-button
                      id="move-after"
                      title="Move card after"
                      icon="hass:arrow-right"
                      ?disabled=${e===t-1}
                      @click=${this._handleMove}
                    ></paper-icon-button>

                    <paper-icon-button
                      icon="hass:delete"
                      @click=${this._handleDeleteCard}
                    ></paper-icon-button>
                  </div>

                  <hui-card-editor
                    .hass=${this.hass}
                    .value="${this._config.cards[e]}"
                    .lovelace=${this.lovelace}
                    @config-changed="${this._handleConfigChanged}"
                  ></hui-card-editor>
                `:i.f`
                  <hui-card-picker
                    .hass=${this.hass}
                    .lovelace=${this.lovelace}
                    @config-changed="${this._handleCardPicked}"
                  ></hui-card-picker>
                `}
        </div>
      </div>
    `}},{kind:"method",key:"_handleSelectedCard",value:function(e){this._selectedCard="add-card"===e.target.id?this._config.cards.length:parseInt(e.target.selected,10)}},{kind:"method",key:"_handleConfigChanged",value:function(e){e.stopPropagation(),this._config&&(this._config.cards[this._selectedCard]=e.detail.config,Object(o.a)(this,"config-changed",{config:this._config}))}},{kind:"method",key:"_handleCardPicked",value:function(e){if(e.stopPropagation(),!this._config)return;const t=e.detail.config;this._config.cards.push(t),Object(o.a)(this,"config-changed",{config:this._config})}},{kind:"method",key:"_handleDeleteCard",value:function(){this._config&&(this._config.cards.splice(this._selectedCard,1),this._selectedCard=Math.max(0,this._selectedCard-1),Object(o.a)(this,"config-changed",{config:this._config}))}},{kind:"method",key:"_handleMove",value:function(e){if(!this._config)return;const t=this._selectedCard,r="move-before"===e.target.id?t-1:t+1,i=this._config.cards.splice(this._selectedCard,1)[0];this._config.cards.splice(r,0,i),this._selectedCard=r,Object(o.a)(this,"config-changed",{config:this._config})}},{kind:"get",static:!0,key:"styles",value:function(){return i.c`
      .toolbar {
        display: flex;
        --paper-tabs-selection-bar-color: var(--primary-color);
        --paper-tab-ink: var(--primary-color);
      }
      paper-tabs {
        display: flex;
        font-size: 14px;
        flex-grow: 1;
      }
      #add-card {
        max-width: 32px;
        padding: 0;
      }

      #card-options {
        display: flex;
        justify-content: flex-end;
        width: 100%;
      }

      #editor {
        border: 1px solid var(--divider-color);
        padding: 12px;
      }
      @media (max-width: 450px) {
        #editor {
          margin: 0 -12px;
        }
      }
    `}}]}},i.a)}}]);
//# sourceMappingURL=chunk.07da9babd817f61e5ac5.js.map
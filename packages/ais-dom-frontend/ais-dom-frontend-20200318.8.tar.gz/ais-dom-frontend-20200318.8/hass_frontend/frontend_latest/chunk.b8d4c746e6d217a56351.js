(self.webpackJsonp=self.webpackJsonp||[]).push([[106],{191:function(a,e,s){"use strict";var o=s(8);e.a=Object(o.a)(a=>(class extends a{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(a){return a}}))},818:function(a,e,s){"use strict";s.r(e);s(237),s(162),s(119);var o=s(4),t=s(32),n=(s(164),s(106),s(324),s(191));customElements.define("ha-config-ais-dom-control",class extends(Object(n.a)(t.a)){static get template(){return o.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }

        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }

        .narrow .border {
          max-width: 640px;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <div class="content">
            <ha-config-section is-wide="[[isWide]]">
              <span slot="header">Konfiguracja bramki AIS dom</span>
              <span slot="introduction"
                >Tutaj możesz skonfigurować parametry bramki AIS dom. Pracujemy
                nad tym, żeby wszystkie opcje bramki można było łatwo
                konfigurować z interfejsu użytkownika.
              </span>

              <ha-config-ais-dom-navigation
                hass="[[hass]]"
                show-advanced="[[showAdvanced]]"
              ></ha-config-ais-dom-navigation>
            </ha-config-section>
          </div>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean}}computeClasses(a){return a?"content":"content narrow"}})}}]);
//# sourceMappingURL=chunk.b8d4c746e6d217a56351.js.map
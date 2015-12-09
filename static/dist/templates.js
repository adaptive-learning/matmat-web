angular.module('matmat').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('simulators/counter-wizard.html',
    "<div id=\"counter\">\n" +
    "\n" +
    "<div ng-repeat=\"p in current track by $index\" ng-class=\"{green: p==1, 'shine-small': p==2, 'shine': p==3, red: p==-1}\" ><div></div></div>\n" +
    "\n" +
    "\n" +
    "</div>"
  );


  $templateCache.put('simulators/counting/simulator.html',
    "<style>\n" +
    "    table#counting-simulator{\n" +
    "        margin:auto;\n" +
    "        background: none;\n" +
    "        border: none;\n" +
    "        margin-top: 10px;\n" +
    "    }\n" +
    "    table#counting-simulator td{ font-size: 3rem; text-align: center;}\n" +
    "    table#counting-simulator td.eq{ width: 2rem; }\n" +
    "    table#counting-simulator td.re{ width: 10rem; text-align: left; }\n" +
    "    table#counting-simulator cubes > div{margin-top: 10px;}\n" +
    "</style>\n" +
    "\n" +
    "<table id=\"counting-simulator\">\n" +
    "    <tr ng-show=\"data.with_text || block\">\n" +
    "        <td ng-repeat=\"part in data.question track by $index\" ng-hide=\"block\">\n" +
    "            <div ng-show=\"type(part) == 'number'\"> {{ part }}</div>\n" +
    "            <span ng-show=\"type(part) == 'string'\"></span>\n" +
    "        </td>\n" +
    "        <td ng-show=\"block\"></td>\n" +
    "        <td ng-show=\"block\">{{ data.question.2 }}</td>\n" +
    "        <td ng-show=\"block\"></td>\n" +
    "        <td class=\"eq\"></td>\n" +
    "        <td class=\"re\"></td>\n" +
    "    </tr>\n" +
    "    <tr>\n" +
    "        <td ng-repeat=\"part in data.question track by $index\" ng-hide=\"block\">\n" +
    "            <div ng-show=\"type(part) == 'number'\"> <cubes ng-class=\"{negative: $index === 2 &&  data.question.1 === '-'}\" size=\"size\" count=\"part\"></cubes> </div>\n" +
    "            <span ng-show=\"type(part) == 'string'\"> {{ part }} </span>\n" +
    "        </td>\n" +
    "        <td ng-show=\"block\">{{ data.question.0 }}</td>\n" +
    "        <td ng-show=\"block\"><cubes width=\"data.question.2\" height=\"data.question.0\"></cubes></td>\n" +
    "        <td ng-show=\"block\">{{ data.question.join(\" \") }}</td>\n" +
    "        <td class=\"eq\"> =  </td>\n" +
    "        <td class=\"re\">\n" +
    "            <responsespan answer=\"data.answer\" response=\"response.value\" solved=\"solved\" />\n" +
    "        </td>\n" +
    "    </tr>\n" +
    "</table>\n" +
    "\n" +
    "<div style=\"height:30px;\"></div>\n" +
    "<responseinput ng-model=\"response.value\" submit=\"submit()\" ng-change=\"change()\" />"
  );


  $templateCache.put('simulators/cubes.html',
    "<div class=\"objects\" ng-show=\"count\" ng-class=\"{selectable: selectable}\" ng-mouseleave=\"hover(0)\">\n" +
    "    <div ng-repeat=\"i in repeater(count) track by $index\" ng-mouseenter=\"hover($index + 1)\" ng-click=\"select($index + 1)\"></div>\n" +
    "</div>\n" +
    "<div class=\"block-objects\" ng-show=\"height && width\">\n" +
    "    <div ng-repeat=\"i in repeater(height) track by $index\">\n" +
    "        <div ng-repeat=\"j in repeater(width) track by $index\"></div>\n" +
    "    </div>\n" +
    "</div>\n" +
    "<div class=\"block-objects\" ng-show=\"field\">\n" +
    "    <div ng-repeat=\"row in field track by $index\">\n" +
    "        <div ng-repeat=\"cube in row track by $index\" ng-class=\"{hide: cube == 0}\"></div>\n" +
    "    </div>\n" +
    "</div>"
  );


  $templateCache.put('simulators/example/simulator.html',
    "data from database: {{ data }}\n" +
    "<br/><br/>\n" +
    "<input class=\"button\" type=\"button\" ng-click=\"answer(true)\" value=\"Správně\" />\n" +
    "<input class=\"button\" type=\"button\" ng-click=\"answer(false)\" value=\"Špatně\" />"
  );


  $templateCache.put('simulators/field/simulator.html',
    "<style>\n" +
    "    table#field-simulator{\n" +
    "        margin:auto;\n" +
    "        background: none;\n" +
    "        border: none;\n" +
    "        margin-top: 10px;\n" +
    "    }\n" +
    "    table#field-simulator td{ font-size: 3rem; text-align: center;}\n" +
    "    table#field-simulator td.eq{ width: 2rem; }\n" +
    "    table#field-simulator td.re{ width: 20rem; text-align: left; }\n" +
    "</style>\n" +
    "\n" +
    "<table id=\"field-simulator\">\n" +
    "    <tr>\n" +
    "        <td><cubes field=\"field\"></cubes></td>\n" +
    "        <td class=\"eq\"></td>\n" +
    "        <td class=\"re\">{{ data.text }} = <responsespan answer=\"data.answer\" response=\"response.value\" solved=\"solved\" /></td>\n" +
    "    </tr>\n" +
    "</table>\n" +
    "\n" +
    "<responseinput ng-model=\"response.value\" submit=\"submit()\" ng-change=\"change()\" />\n"
  );


  $templateCache.put('simulators/fillin/simulator.html',
    "<h2>{{ data.pre }}<span style=\"color: blue\"><responsespan answer=\"data.answer\" response=\"answer.value\" solved=\"solved\" def=\"_\"/></span>{{ data.post }}</h2>\n" +
    "<responseinput ng-model=\"answer.value\" submit=\"check_answer()\" ng-change=\"change()\" />"
  );


  $templateCache.put('simulators/free_answer/simulator.html',
    "<h2 class=\"row collapse\">\n" +
    "    <div class=\"small-7 medium-6 text-right columns\">{{ data.question }}</div>\n" +
    "    <div class=\"small-2 medium-2 text-center columns\">&nbsp;=&nbsp;</div>\n" +
    "    <div class=\"small-3 medium-4 text-left columns\"><responsespan answer=\"data.answer\" response=\"answer.value\" solved=\"solved\" /></div>\n" +
    "</h2>\n" +
    "<responseinput ng-model=\"answer.value\" submit=\"check_answer()\" ng-change=\"change()\" />"
  );


  $templateCache.put('simulators/keyboard-wizard.html',
    "<div keypress-events id=\"keyboard-wizard\" class=\"unselectable\" ng-class=\"{open: global.keyboard != 'gone' && global.keyboard != 'empty' && !closed && !global.hide_question}\">\n" +
    "    <div id=\"scroll-left\"></div><div id=\"scroll-center\">\n" +
    "        <div id=\"scroll-content\">\n" +
    "            <div>\n" +
    "                <div class=\"key left back\" ng-cloak ng-show=\"global.keyboard == 'full'\" ng-click=\"add_text('larr')\"><i class=\"fi-arrow-left\"></i></div>\n" +
    "                <div class=\"key right submit\" ng-cloak ng-click=\"submit()\" ng-class=\"{disabled: !global.input.value}\"><i class=\"fi-check\"></i></div>\n" +
    "\n" +
    "                <div class=\"choices\"  ng-cloak ng-show=\"global.keyboard == 'full'\">\n" +
    "                    <div class=\"key\" ng-repeat=\"choice in choices\" ng-click=\"add_text(choice)\" >{{ choice }}</div>\n" +
    "                </div>\n" +
    "                <div class=\"choices\" ng-cloak ng-show=\"global.keyboard == 'choices'\">\n" +
    "                    <div class=\"key choice\" ng-repeat=\"choice in global.choices\" ng-click=\"choose_answer(choice)\" >{{ choice }}</div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div><div id=\"scroll-right\"></div>\n" +
    "    <div class=\"key skip\" style=\"margin-left: -165px; position:absolute; top: 150px;\" ng-click=\"skip()\">přeskočit</div>\n" +
    "    <div ng-cloak next-action=\"global.hide_question\" ng-show=\"global.hide_question\" class=\"blink key hide\" style=\"margin-left: 5px; position:absolute; top: 80px;\" ng-click=\"global.hide_question()\"><i class=\"fi-arrow-right\"></i></div>\n" +
    "</div>\n"
  );


  $templateCache.put('simulators/keyboard.html',
    "<div id=\"keyboard\" ng-hide=\"global.keyboard == 'gone' || global.simulator_active == false\">\n" +
    "    <p ng-click=\"switch_visibility()\" class=\"keyboard-text\" ng-cloak ng-hide=\"true\">\n" +
    "        {{ text }}\n" +
    "        <span ng-hide=\"hidden\">Skrýt</span>\n" +
    "        <span ng-show=\"hidden\">Zobrazit klávesnici</span>\n" +
    "    </p>\n" +
    "    <div id=\"keyboard-buttons\" ng-hide=\"hidden\">\n" +
    "        <div ng-cloak ng-show=\"global.keyboard == 'full'\" class=\"small-8 medium-6 large-4 small-centered column\">\n" +
    "            <div>\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"1\" ng-click=\"add_text('1')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"2\" ng-click=\"add_text('2')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"3\" ng-click=\"add_text('3')\" />\n" +
    "                <div></div>\n" +
    "            </div>\n" +
    "            <div>\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"4\" ng-click=\"add_text('4')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"5\" ng-click=\"add_text('5')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"6\" ng-click=\"add_text('6')\" />\n" +
    "                <div></div>\n" +
    "            </div>\n" +
    "            <div>\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"7\" ng-click=\"add_text('7')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"8\" ng-click=\"add_text('8')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"9\" ng-click=\"add_text('9')\" />\n" +
    "                <div></div>\n" +
    "            </div>\n" +
    "            <div>\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\".\" ng-click=\"add_text('.')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"0\" ng-click=\"add_text('0')\" />\n" +
    "                <input type=\"button\" class=\"button numpad small-4 columns\" value=\"&larr;\" ng-click=\"add_text('larr')\" />\n" +
    "                <div></div>\n" +
    "            </div>\n" +
    "            <div>\n" +
    "                <input type=\"button\" class=\"button numpad small-8 small-offset-4 columns tick\" value=\"\" ng-click=\"submit()\" />\n" +
    "            </div>\n" +
    "            <div>\n" +
    "                <input type=\"button\" class=\"button numpad small-8 small-offset-4 columns show-for-small-only\" value=\"Nevím\" ng-click=\"skip()\" />\n" +
    "            </div>\n" +
    "        </div>\n" +
    "\n" +
    "        <div ng-cloak ng-show=\"global.keyboard == 'choices'\" class=\"text-center choices\">\n" +
    "            <input type=\"button\" class=\"button numpad small-1\"\n" +
    "                   value=\"{{ choice }}\" ng-repeat=\"choice in global.choices\"\n" +
    "                   ng-click=\"submit_answer(choice)\"\n" +
    "                    />\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>"
  );


  $templateCache.put('simulators/numberline/simulator.html',
    "<!--suppress CheckEmptyScriptTag -->\n" +
    "<h2>{{ data.question }} </h2>\n" +
    "\n" +
    "<svg ng-attr-width=\"{{ settings.width }}\" ng-attr-height=\"{{ settings.height + 20 * (range.1 > 20) }}\">\n" +
    "    <defs>\n" +
    "        <filter id=\"shadow\" x=\"-50%\" y=\"-50%\" width=\"200%\" height=\"200%\">\n" +
    "          <feGaussianBlur  in=\"SourceGraphic\" stdDeviation=\"2\" />\n" +
    "        </filter>\n" +
    "      </defs>\n" +
    "\n" +
    "\n" +
    "    <line ng-attr-x1=\"{{ settings.offset }}\" ng-attr-y1=\"{{ settings.top }}\" ng-attr-x2=\"{{ settings.width - settings.offset }}\" ng-attr-y2=\"{{ settings.top }}\" style=\"stroke: black; stroke-width:1\" />\n" +
    "    <g\n" +
    "            id=\"point{{ point.number }}\"\n" +
    "            class=\"numberline-point\"\n" +
    "            ng-repeat=\"point in points\"\n" +
    "            onclick=\"angular.element(this).scope().select(this)\"\n" +
    "            onmouseover=\"angular.element(this).scope().hover(this)\"\n" +
    "            onmouseleave=\"angular.element(this).scope().leave()\"\n" +
    "            >\n" +
    "        <circle class=\"shadow\" class=\"numberline-point\" ng-attr-cx=\"{{ point.x }}\" ng-attr-cy=\"{{ point.y }}\" ng-attr-r=\"{{ point.r*2 }}\" filter=\"url(#shadow)\"/>\n" +
    "        <circle class=\"point\" class=\"numberline-point\" ng-attr-cx=\"{{ point.x }}\" ng-attr-cy=\"{{ point.y }}\" ng-attr-r=\"{{ point.r }}\" fill=\"grey\"/>\n" +
    "        <rect onmousedown=\"return false\" ng-attr-width=\"{{ settings.hover_size }}\" ng-attr-height=\"{{ settings.hover_size }}\" ng-attr-x=\"{{ point.x-settings.hover_size/2}}\" ng-attr-y=\"{{ point.y -settings.hover_size/2}}\" />\n" +
    "        <text ng-attr-x=\"{{ point.x }}\" ng-attr-y=\"{{ point.y + 20 + 20 * (point.number % 2) * (range.1 > 20)}}\" text-anchor=\"middle\" display=\"{{ point.display }}\">{{ point.number }}</text>\n" +
    "    </g>\n" +
    "    <rect ng-show=\"rect.number < hovered_number\" style=\"fill: #ff5913\" ng-repeat=\"rect in rects\" ng-attr-height=\"{{ rect.size }}\" ng-attr-width=\"{{ rect.size }}\" ng-attr-x=\"{{ rect.x }}\" ng-attr-y=\"{{ rect.y }}\"/>\n" +
    "</svg>\n" +
    "<br/>\n" +
    "<form ng-submit=\"check_answer()\" ng-hide=\"simple\">\n" +
    "    <div style=\"height: 74px\">\n" +
    "        <input ng-hide=\"okShow || nokShow\" class=\"button tick\" ng-disabled=\"!selected_number && selected_number!=0\" type=\"submit\" value=\"&nbsp;\" />\n" +
    "    </div>\n" +
    "</form>"
  );


  $templateCache.put('simulators/pairing/simulator.html',
    "<br>\n" +
    "<div>\n" +
    "    <div ng-repeat=\"row in rows\">\n" +
    "        <input class=\"pairing-button\" ng-class=\"'pairing-' + cell.state\" type=\"button\" \n" +
    "        ng-repeat=\"cell in row\" value=\"{{cell.text}}\" ng-click=\"click(cell)\" \n" +
    "        ng-disabled=\"cell.disabled || gameover\"/>\n" +
    "    </div>\n" +
    "</div>\n"
  );


  $templateCache.put('simulators/response-input.html',
    "<form ng-submit=\"local_submit()\" ng-hide=\"global.keyboard == 'choices'\">\n" +
    "    <div class=\"row collapse hide-for-small-only\">\n" +
    "        <div class=\"small-8 small-offset-1 medium-5 medium-offset-3 large-3 large-offset-4 columns\">\n" +
    "            <input class=\"active\" ng-disabled=\"!global.simulator_active\" id=\"simulator-input\" type=\"text\" focus-me=\"global.simulator_active\" ng-change=\"change()\" ng-model=\"ngModel\" autocomplete=\"off\" placeholder=\"Zadej svoji odpověď\"/>\n" +
    "        </div>\n" +
    "        <div class=\"small-2 large-1 columns\">\n" +
    "            <input class=\"button postfix tick\" ng-class=\"{disabled: !global.input.value}\" type=\"submit\" value=\"\" />\n" +
    "        </div>\n" +
    "        <div></div>\n" +
    "    </div>\n" +
    "</form>\n"
  );


  $templateCache.put('simulators/response-span.html',
    "<span ng-hide=\"response\">{{ def }}</span>\n" +
    "<span ng-hide=\"solved\">{{ response }}</span>\n" +
    "<span ng-show=\"solved && answer!=response\" class=\"red\" style=\"text-decoration: line-through\">{{ response }}</span>\n" +
    "<span ng-cloak ng-show=\"solved\" class=\"green\">{{ answer }}</span>"
  );


  $templateCache.put('simulators/roller-wizard.html',
    "<div id=\"roller-wizard\" ng-class=\"{closed: closed}\">\n" +
    "    <div id=\"roller-top\">{{ question }}</div>\n" +
    "    <div id=\"roller-playground\">\n" +
    "        <div ng-transclude>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "    <div id=\"roller-bottom\"></div>\n" +
    "</div>"
  );


  $templateCache.put('simulators/selecting/simulator.html',
    "<h2>{{data.question}}</h2>\n" +
    "<cubes count=\"data.nrows * 10\" input=\"selected\" correct=\"correct\"></cubes>\n" +
    "<div style=\"height:30px;\"></div>\n" +
    "<form ng-submit=\"submit()\" ng-hide=\"simple\">\n" +
    "    <div class=\"row collapse\">\n" +
    "        <div class=\"small-1 small-centered columns\">\n" +
    "            <input class=\"button postfix tick\" ng-disabled=\"selected==0\" type=\"submit\" value=\"&nbsp;\" />\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</form>\n"
  );


  $templateCache.put('simulators/simulator_selector.html',
    "<div class=\"switch radius small\" ng-repeat=\"simulator in simulators\">\n" +
    "    <input ng-model=\"simulator.selected\" id=\"simulator{{ simulator.pk }}\" ng-change=\"change(simulator)\" type=\"checkbox\">\n" +
    "    <label for=\"simulator{{ simulator.pk }}\"></label>\n" +
    "    <span>{{ simulator.note }}</span>\n" +
    "</div>\n"
  );


  $templateCache.put('simulators/visualization/simulator.html',
    "<h2 class=\"row collapse\">\n" +
    "    <div class=\"small-7 medium-6 text-right columns\">{{ data.question[0] }}</div>\n" +
    "    <div class=\"small-2 medium-2 text-center columns\">&nbsp;=&nbsp;</div>\n" +
    "    <div class=\"small-3 medium-4 text-left columns\"><responsespan answer=\"data.answer\" response=\"answer.value\" solved=\"solved\" /></div>\n" +
    "</h2>\n" +
    "<div class=\"row collapse\">\n" +
    "    <div class=\"apple columns\" ng-repeat=\"apple in apples track by $index\" ng-attr-id=\"{{'apple' + $index}}\" ></div>\n" +
    "    <div class=\"columns\"></div>\n" +
    "</div>\n" +
    "<div class=\"row collapse\">\n" +
    "    <div class=\"basket columns\" ng-repeat=\"basket in baskets track by $index\" ng-attr-id=\"{{'basket' + $index}}\"></div>\n" +
    "    <div class=\"columns\"></div>\n" +
    "</div>\n" +
    "<responseinput ng-model=\"answer.value\" submit=\"check_answer()\" ng-change=\"change()\" />\n"
  );


  $templateCache.put('graphics/wizard/wizard.html',
    "<div id=\"wizard\">\n" +
    "    <div id=\"guy\"></div>\n" +
    "\n" +
    "    <div ng-cloak ng-show=\"say || old_say\"><div ng-show=\"say\" class=\"animate-show\">\n" +
    "        <div id=\"wizard-bubble2\"></div>\n" +
    "        <div id=\"wizard-bubble1\"></div>\n" +
    "        <div id=\"wizard-bubble\">{{ say }}{{ old_say }}</div>\n" +
    "    </div></div>\n" +
    "</div>"
  );

}]);

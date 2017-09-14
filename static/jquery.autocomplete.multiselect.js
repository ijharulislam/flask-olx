// http://jsfiddle.net/mekwall/sgxKJ/

$.widget("ui.autocomplete", $.ui.autocomplete, {
    options : $.extend({}, this.options, {
        multiselect: false
    }),
    _create: function(){
        this._super();

        var self = this,
            o = self.options;

        if (o.multiselect) {
            console.log('multiselect true');

            self.selectedItems = {};           
            self.multiselect = $("<div></div>")
                .addClass("ui-autocomplete-multiselect ui-state-default ui-widget")
                .css("width", self.element.width())
                .insertBefore(self.element)
                .append(self.element)
                .bind("click.autocomplete", function(){
                    self.element.focus();
                });
            
            var fontSize = parseInt(self.element.css("fontSize"), 10);
            function autoSize(e){
                // Hackish autosizing
                var $this = $(this);
                $this.width(1).width(this.scrollWidth+fontSize-1);
            };

            var kc = $.ui.keyCode;
            self.element.bind({
                "keydown.autocomplete": function(e){
                    if ((this.value === "") && (e.keyCode == kc.BACKSPACE)) {
                        var prev = self.element.prev();
                        delete self.selectedItems[prev.text()];
                        prev.remove();
                    }
                },
                // TODO: Implement outline of container
                "focus.autocomplete blur.autocomplete": function(){
                    self.multiselect.toggleClass("ui-state-active");
                },
                "keypress.autocomplete change.autocomplete focus.autocomplete blur.autocomplete": autoSize
            }).trigger("change");

            // TODO: There's a better way?
            o.select = o.select || function(e, ui) {
                $("<div></div>")
                    .addClass("ui-autocomplete-multiselect-item")
                    .text(ui.item.label)
                    .append(
                        $("<span></span>")
                            .addClass("ui-icon ui-icon-close")
                            .click(function(){
                                var item = $(this).parent();
                                delete self.selectedItems[item.text()];
                                item.remove();
                              
                                // if(jQuery.inArray(item.text(), selected_city) !== -1){
                                //     var i = selected_city.indexOf(item.text());
                                //     if(i != -1) {
                                //         selected_city.splice(i, 1);
                                //     }
                                //     console.log("Selected City", selected_city);
                                //     getSuburb(selected_city);
                                // }

                                if(item.text()==selected_city){
                                    selected_city = "";
                                }


                                // if(jQuery.inArray(item.text(), selected_suburb) !== -1){
                                //     var i = selected_suburb.indexOf(item.text());
                                //     if(i != -1) {
                                //         selected_suburb.splice(i, 1);
                                //     }
                                // }

                                if(item.text()==selected_suburb){
                                    selected_suburb = "";
                                }

                                // if(jQuery.inArray(item.text(), selected_categ) !== -1){
                                //     var i = selected_categ.indexOf(item.text());
                                //     if(i != -1) {
                                //         selected_categ.splice(i, 1);
                                //     }
                                //     getSubCategory(selected_categ)
                                // }

                                if(item.text()==selected_categ){
                                    selected_categ = "";
                                }

                                // if(jQuery.inArray(item.text(), selected_subcateg) !== -1){
                                //     var i = selected_subcateg.indexOf(item.text());
                                //     if(i != -1) {
                                //         selected_subcateg.splice(i, 1);
                                //     }
                                // }

                                if(item.text()==selected_subcateg){
                                    selected_subcateg = "";
                                }

                                if(jQuery.inArray(item.text(), selected_fields) !== -1){
                                    var i = selected_fields.indexOf(item.text());
                                    if(i != -1) {
                                        selected_fields.splice(i, 1);
                                    }
                                }
                            })
                    )
                    .insertBefore(self.element);
                
                self.selectedItems[ui.item.label] = ui.item;
                self._value("");
                return false;
            }

            /*self.options.open = function(e, ui) {
                var pos = self.multiselect.position();
                pos.top += self.multiselect.height();
                self.menu.element.position(pos);
            }*/
        }

        return this;
    }
});
require.undef('sentinel_table_description_widget');

define('sentinel_table_description_widget', ["@jupyter-widgets/base"], function(widgets) {

    var SentinelTableDescriptionWidget = widgets.DOMWidgetView.extend({

        // Render the view.
        render: function()
        {
            this.table_output = document.createElement('TABLE');
            this.table_output.disabled = this.model.get('disabled');

            this.entry_data = this.model.get('entry_list');
            this.description_data = this.model.get('entry_descriptions');
            this.description_metadata = this.model.get('entry_descriptions_metadata');
            this.class_type = this.model.get('class_list');
            this.table_header = this.model.get('table_header');
            this.expandable = this.model.get('expandable');

            this.selected_entry = null;

            this.toggle_class_list(this.table_output);
            this.update_list();

            this.el.appendChild(this.table_output);

            // Python -> JavaScript update
            this.model.on('change:entry_list', this.entries_changed, this);
            this.model.on('change:entry_descriptions', this.entries_changed, this);
            this.model.on('change:class_list', this.classes_changed, this);
            this.model.on('change:disabled', this.disabled_changed, this);
            this.model.on('change:reset_flag', this.clear_selection, this);

            // JavaScript -> Python update
            this.table_output.onchange = this.input_changed.bind(this);
        },

        toggle_class_list: function(elem)
        {
            for (var j = 0; j < this.class_type.length; j++)
            {
                elem.classList.toggle(this.class_type[j]);
            }
        },

        toggle_selection: function(elem)
        {
            elem.classList.toggle("desc-selected");
            var div = elem.firstChild.childNodes[1];
            div.classList.toggle("desc-selected");
            this.display_logic(div);
        },

        display_logic: function(elem)
        {
            if (elem.classList.contains("desc-selected") || elem.classList.contains("toggle_expanded_self"))
            {
                if (elem.classList.contains("hide-display"))
                {
                    elem.classList.toggle("hide-display")
                }
            }
            else
            {
                if (!elem.classList.contains("hide-display"))
                {
                    elem.classList.toggle("hide-display")
                }
            }
        },

        clear_selection: function()
        {
            if (this.selected_entry !== null)
            {
                this.toggle_selection(this.selected_entry);
            }
            this.model.set('selected_value_index', -1);
            this.model.save_changes();
            this.selected_entry = null;
        },

        select_entry: function(elem, index)
        {
            if (this.selected_entry !== null)
            {
                this.toggle_selection(this.selected_entry);
            }
            if (this.selected_entry == elem)
            {
                this.model.set('selected_value_index', -1);
                this.model.save_changes();
                this.selected_entry = null;
                return false;
            }
            this.toggle_selection(elem);
            this.selected_entry = elem;
            this.model.set('selected_value_index', index);
            this.model.save_changes();
            return false;
        },

        expand_entry: function(elem1, elem2, elem3)
        {
            elem1.classList.toggle("toggle_expanded_self");
            elem2.classList.toggle("toggle_expanded_self");
            elem3.classList.toggle("toggle_expanded_self");
            this.display_logic(elem3);
        },


        update_list: function()
        {
          let st = this;
          let tr = document.createElement('tr');
          var th = document.createElement('th');
          var tn = document.createTextNode(this.table_header);

          this.toggle_class_list(tr);
          this.toggle_class_list(th);

          tr.appendChild(th);
          th.appendChild(tn);

          this.table_output.appendChild(tr)

          for (let i = 0; i < this.entry_data.length; i++)
          {
                var index = i;
                let tr = document.createElement('tr');
                let td = document.createElement('td');
                let tiv = document.createElement('div');

                this.toggle_class_list(td);
                this.toggle_class_list(tr);
                this.toggle_class_list(tiv);

                tr.appendChild( td );
                td.appendChild( document.createTextNode(this.entry_data[i]) );
                td.appendChild( tiv );
                tiv.appendChild( document.createTextNode(this.description_data[i]) );
                tiv.classList.toggle("table-expanded-description");
                tiv.classList.toggle("hide-display");

                if(this.expandable)
                {
                    tr.onclick = function () { return st.expand_entry(tr, td, tiv) };
                }
                tr.oncontextmenu = function() { return st.select_entry(this, i); };

                this.table_output.appendChild(tr);
            }
        },

        entries_changed: function()
        {
            while (this.table_output.firstChild)
            {
                this.table_output.firstChild.remove();
            }
            this.description_data = this.model.get('entry_descriptions');
            this.entry_data = this.model.get('entry_list');
            this.update_list();
        },

        disabled_changed: function()
        {
            this.table_output.disabled = this.model.get('disabled');
        },

        input_changed: function()
        {
            this.model.set('value', this.table_output.value);
            this.model.save_changes();
        },

        classes_changed: function()
        {
            this.toggle_class_list(this.table_output);
            this.class_type = this.model.get('class_list');
            this.toggle_class_list(this.table_output);
        },

    });

    return {
        SentinelTableDescriptionWidget: SentinelTableDescriptionWidget
    };
});
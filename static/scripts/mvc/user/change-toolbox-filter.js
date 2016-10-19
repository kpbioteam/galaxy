define(["mvc/form/form-view","mvc/ui/ui-misc"],function(a,b){return Backbone.View.extend({initialize:function(c){var d=this;this.model=c&&c.model||new Backbone.Model(c),this.form=new a({title:"Manage Toolbox Filters",name:"toolbox_filter",inputs:c.inputs,operations:{back:new b.ButtonIcon({icon:"fa-caret-left",tooltip:"Return to user preferences",title:"Preferences",onclick:function(){d.remove(),c.onclose()}})},buttons:{save:new b.Button({tooltip:"Save changes",title:"Save changes",cls:"ui-button btn btn-primary",floating:"clear",onclick:function(){d._save()}})}}),this.setElement(this.form.$el)},_save:function(){var a=this;$.ajax({url:Galaxy.root+"api/user_preferences/"+Galaxy.user.id+"/toolbox_filters",type:"PUT",data:a.form.data.create()}).done(function(b){a.form.message.update({message:b.message,status:"success"})}).fail(function(b){a.form.message.update({message:b.responseJSON.err_msg,status:"danger"})})}})});
//# sourceMappingURL=../../../maps/mvc/user/change-toolbox-filter.js.map
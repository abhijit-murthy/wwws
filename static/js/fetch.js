function get_groups(token){
	$.getJSON("/get_groups",{
		access_token: token
	},function(data){
		groups = data.groups;
		list = '';
		for(var i = 0;i<groups.length;i++){
			list += '<p>'+groups[i].groupName+'</p>'
		}
		$('.groups').append(list);
	});
}
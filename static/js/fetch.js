function get_groups(token){
	$.getJSON("/get_groups",{
		access_token: token
	},function(data){
		groups = data.groups;
		list = '';
		for(var i = 0;i<groups.length;i++){
			href = '/?access_token=' + token + "&groupid=" + groups[i].groupID + "&state=2";
			console.log(href);
			list += "<p><a href='" + href + "'>" + groups[i].groupName + "<a></p>";
		}
		$('.groups').append(list);
	});
}
function generate_message(token,gid){
	$.getJSON('/generate_message',{
		access_token:token,
		groupid: gid
	},function(data){
		console.log(data);
		$('.message').prepend("<p>"+data.sentence.sentence+"</p>");
	});
}
var http = require('http');
var fs = require('fs');
var escape = require('escape-html');
var redis = require("redis"),
client = redis.createClient();
var pg = require('pg');
var conString = "postgres://omgbbqhax:invicible92@localhost/nearanodb";

var server = http.createServer(function (req, res) {
	var username = req.url;
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end('i love node.- Yasin Aktimur\n');
        
}).listen(8888);


var io = require('socket.io').listen(server);

io.sockets.on('connection', function (x) {
    
x.on('load', function (channelname , userimage) {
	x.join(channelname);
	
	client.hmset(x.id, "username", x.id , "image", userimage , "sck" , channelname);
	
	
	
	
	
	
x.on('disconnect', function(){
        console.log("Connection " + x.id + " terminated.");
	client.hgetall(x.id , function (err, obj) {
	if (obj.image == "http://nearano.com/static/images/ano.png") {
	//çıkan kişi anonim
	io.to(x.rooms[1]).emit('userDisc', x.id);
	
	}else {
	io.to(x.rooms[1]).emit('anonDisc', x.id );	
	
	pg.connect(conString, function(err, client, done) {
	  if(err) {
	    return console.error('error fetching client from pool', err);
	  }
	  
	  
	  client.query("UPDATE twitter_auth_account  SET status ='offline' WHERE username='"+obj.sck+"';",  function(err, result) {
	    done();
	
	    if(err) {
	      return console.error('error running query', err);
	    }
	   console.log(obj.sck);
	   
	   
	  });
	});
	
	}	
	});
	
	
	//io.to(x.rooms[1]).emit('shareMsg', x.id, "User disconnect", x.id , "http://nearano.com/static/images/disconnect.jpg");
});	
	
	
});

//usersender profil sahibinin gönderdiklerini kapsar dolayısıyla kendisinin görmesinde gerek yoktur 
x.on('userSender', function (msg, receiver) {
escapedmsg2 = escape(msg)
client.hgetall(x.id , function (errr, objj) {

client.hgetall(receiver , function (err, obj) {
	
console.log("jjj : "+  obj.username);
if (io.sockets.connected[obj.username]) {
io.sockets.connected[obj.username].emit('shareMsg', x.id, escapedmsg2, objj.username, objj.image);
}
});

});

});

	
	
//bu kısım socket.send ile çalışır ve diğerlerinden gelen veriyi alır dolayısıyla buradan gelenleri ancak kullanıcı görmelidir
x.on('message', function (msg) {
escapedmsg = escape(msg)
client.hgetall(x.id , function (err, obj) {
console.log(obj.image);
io.to(x.rooms[1]).emit('myMsg', x.id, escapedmsg, obj.username, obj.image);
});
	  
  });
  
  //socket.on('disconnect', function () { });
});




console.log('Server running at --> http://127.0.0.1:1337/');
<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
  <link rel="icon" href="">
  <link rel="stylesheet" type="text/css" href="login.css">
  
</head>
<body>
<h1 class="net">MovieDB</h1>
 <div id="log">
  <h1>SIGN IN</h1>
  <form method='post' action='' id='form' target="_self">
  LOGIN ID :<br><input type='text' id='username' placeholder='username'><br><br>
  PASSWORD :<br><input type='password' id='password' placeholder='password'><br><br>
  <input type="button" class="but" value="Login" onclick="submitfrom()"><br> <br>
 </form>

 </div>

  <div id="log1">
  <h1>REGISTER</h1>
  <form method='post' action='pass.php' id='form1'>
  USERNAME :<br><input type='text' name='id' placeholder='username' id="username1"><br>
  E-MAIL : <br><input type="E-MAIL" name="mail" placeholder='email' id="mail1"><br>
  Mobile-no : <br><input type="text" name="phno" placeholder='phno' id="phno1"><br>
  PASSWORD :<br><input type='password' name='password' placeholder='password' id="password1"><br>
  CONFIRM PASSWORD:<br><input type='password' name='CNFpassword' placeholder='password' id="cnfpssd"><br>
  <input type="button" class="but" value="Register" onclick="registerfrom()"><br>
  <br><br>
 </form>
</div>
</body>
<script>
  var link = "http://localhost:5000";
    function submitfrom(){
        var password = document.getElementById("password").value;
        var username =document.getElementById("username").value;
        //alert(password)
        var url = link+"/webtech2/l";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200)
            {
              alert("request sucessfull");
              var json =JSON.parse(xhttp.responseText);
              console.log(json["usn"])
             setCookie("username",json["usn"],1)

              alert("done")
              location.replace("home.html")
            }
            if(this.readyState==4 && this.status!=200){
            console.log("authentication failure")
            var json =JSON.parse(xhttp.responseText);
              //console.log(json)


            
            alert("error")
            }

        };
        var data=JSON.stringify({"username":username,"pwd":password});
        xhttp.open("POST",url,true);
        xhttp.setRequestHeader("Content-Type","application/json");
        xhttp.send(data);       
    }

    function registerfrom(){
      var password = document.getElementById("password1").value;
        var username =document.getElementById("username1").value;
        var cnfpassword =document.getElementById("cnfpssd").value;
        var phno = document.getElementById("phno1").value;
        var email = document.getElementById("mail1").value;
        //alert("check")
        //console.log(password,username,cnfpassword,phno,email)
        if (password!=cnfpassword) { alert("passwords dont match") }

        var url = link+"/webtech2/r";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200)
            {
              alert("registration sucessfull");
              var json =JSON.parse(xhttp.responseText);
              console.log(json)
              location.replace("login.php")
            }
            if(this.readyState==4 && this.status!=200){
            alert("registration failure")
            var json =JSON.parse(xhttp.responseText);
              console.log(json)
            //var message =document.getElementById("message");
            //message.innerHTML=json;
            //message.style.color="#ff1a1a";
            //location.replace("login.php")
            alert("error")
            }

        };
        var data=JSON.stringify({"username":username,"pwd":password,"phno":phno,"email":email});
        xhttp.open("POST",url,true);
        xhttp.setRequestHeader("Content-Type","application/json");
        xhttp.send(data);


    }


function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


</script>
</html>

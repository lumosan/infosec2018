Lucia Montero Sanchis. Information Security and Privacy, EPFL 2018

# Homework 1

## Exercise 1

By looking at the source code of the webpage I found the Javascript script carrying out the authentication. It is possible to see how the password is computed from the username (see below). By running this I obtained the correct password that allowed me to login and obtain the correct token.

`
function ascii (a) { return a.charCodeAt(0); }
function toChar(i) { return String.fromCharCode(i); }

function superencryption(msg,key) {
    if (key.length < msg.length) {
        var diff = msg.length - key.length;
        key += key.substring(0,diff);
    }

    var amsg = msg.split("").map(ascii);
    var akey = key.substring(0,msg.length).split("").map(ascii);
    return btoa(amsg.map(function(v,i) {
        return v ^ akey[i];
    }).map(toChar).join(""));
}
var mySecureOneTimePad = "Never send a human to do a machine's job";
var username = "lucia.monterosanchis@epfl.ch";
var enc = superencryption(username,mySecureOneTimePad);

enc;
`

------

## Exercise 2

I saw that a cookie was created when clicking on "Login", and that its value varied a lot when logging with different usernames and it was almost the same when using the same username. By logging in with my EPFL address I got:
bHVjaWEubW9udGVyb3NhbmNoaXNAZXBmbC5jaCwxNTE5Mzk1MDE1LGNvbTQwMixodzEsZXgxLHVzZXI

I then converted it from base-64 to UTF, obtaining:
lucia.monterosanchis@epfl.ch,1519395015,com402,hw1,ex1,user

Then I codified the following in base64 form, and modified the cookie with the base-64 value:
lucia.monterosanchis@epfl.ch,1519395097,com402,hw1,ex1,administrator

And obtained the correct cookie (before trying with 'administrator' I tried with 'admin', but it didn't work).


------

## Exercises 3 and 4

The script provided obtains the tokens for exercises 3 and 4 and prints them in the terminal. When printed, tokens are preceded by the exercise they belong to (i.e. 'ex3' or 'ex4'). It can be run from the attacker using python3:

`sudo docker exec -it attacker python3 shared/interceptor.py`
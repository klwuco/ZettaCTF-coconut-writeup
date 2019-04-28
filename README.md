The following challenge is from the [Zetta-CTF](http://php.checksec.sh:8000)  *PHP: Horrific Puzzle*, during the [VXCON](https://www.vxcon.hk) in Hong Kong, 27 Apr - 28 Apr. The challenge is named 🥥.
(btw no one plays)

## Challenge

The code reads

```<?=@preg_match('/^[\(\)\*\-\.\[\]\^]+$/',($_=$_GET["🥥"]))&&!(strlen($_)>>10)?@eval("set_error_handler(function(){exit();});error_get_last()&&exit();return $_;"):!highlight_file(__FILE__);```

In pseudocode, we can write this as

```
if input matches the pattern '/^[\(\)\*\-\.\[\]\^]+$/' and length of input < 1024:
	with exit on error, eval input and print the return value
else:
	show the source code
```

Our goal is to execute ```/checksec.sh``` (the common goal of the whole CTF).

​	In short, we can run wherever we want, but the command need to contain only ```()*-.[]^```, and the command needs to be less than 1024 characters. Also, any error/warning/notice will cause the program to exit.

## Is this JSFuck?

​	The idea of restricting the allowed characters is not new: perhaps the most famous one is JSFuck, which can turn any javascript code into valid js codes, but using ```()[]!+```. Just looking from it, it seems that we are even better off than JSFuck, since we have more characters. But actually no. The reason is that we don't have ```+```, instead we get this awkward charset of ```*-.^```. Even the simplest number ```3``` can only be constructed by ```10-1-1-1-1-1-1-1``` instead of the obvious ```1+1```.

## Constructing the Easy Characters

 With inspirations from JSFuck, trial and error, and the cOnSiStEnT behavior of php , we can begin to assemble some simple characters:

0 can be expressed by ```[]^[]```, and
1 can be expressed by ```[]^[[]]```.

With the help of ```.```, which can act as the concatenation operator for strings, we can express 10 by ```[]^[].[]^[[]]```. Then we can get the other numbers by repeatedly subtract 1 from 10 multiple times.

So for example, 6 is ```10-1-1-1-1``` or equivalently, ```7-1``` , or ```([]^[].[]^[[]])-[]^[[]]-[]^[[]]-[]^[[]]-[]^[[]]```. So we can construct all the numbers we want.

Now we want some English letters. Luckily we have floating point numbers, which has ```INF``` and scientific notations like ```1.234E+45```.  So we now we can use I,N,F,.,E,+ as well. Of course we cannot do something like ```(INF)[0]```  since INF is a number (a float), but we can concatenate a 0 at the back to make it a string, i.e. do ```(INF . 0)[0]```, which is equivalent to ```'INF0'[0]```. At the same time, observe that we can use ```-``` just by using ```(-1 . 0)[0]```.

## Creating the Payload

Now, by using what we have, we can **try** to construct our payload. We should do something like ```exec('/checksec.sh')```. Although we can only input string, not identifiers, doing ```'exec'('/checksec.sh')``` will still result in a function call in php. Also, we can try to reduce the character we use by using filename substitution in bash, i.e. using ```*``` to match our file. So now we can reduce the payload to ```'exec'('/*.*')```. 

Now we need to construct the characters that we need: ```exc/*.```. php functions are case insensitive so "EXC" will also work. It left us to construct "xc/\*". The main technique for doing so is to do xor: 

<center>x=y <b>xor</b> z </center>

, where x is the character we want, and y, z are the characters we have. Notice that

<center>x = y <b>xor</b> z iff x <b>xor</b> y = z</center>

So we can try to xor the characters we want with the characters we have, and hope that we get some characters that we have by some trial-and-error. For example:

<center>'c' <b>xor</b> 'N' = '-', so 'c' = 'N' <b>xor</b> '-', and we have both N and - already.</center>

Another way is to get the characters we want by xor-ing neighboring characters by a small 'number', e.g.:

<center>'*' = '.' <b>xor</b> "\x04" = '.' <b>xor</b> ( '4' xor '0')</center>

. Here we need the string ```'1'``` and ```'5'```, so we need to do ```'.' xor ((4 . 0) xor (0 . 0)) ```.

## PHP behavior LOL

By now we are able to construct all the characters needed for our payload. But if we check the length of our payload, it will be something like 12xx characters (originally with all lower case characters, the payload is 22xx characters long) ! We need to reduce the character count.

Now we turn to the hint by the author:

- There is a shorter payload than ```/*.*```
- 'ABC' **xor** 'bc' = ???
- '/*' can be constructed together in a weird way: **xor** is bitwise and it commutes

For the first hint, notice that we can reduce the payload to just ```/*h```  and it will still expand to ```/checksec.sh``` correctly.

For the second hint, observe that in php, a longer string xor a shorter string gives us a shorter string. In fact, we made use of this fact in ```'*' = '.' xor ((1 . 0) xor (5 xor 0)) ```.

The third hint (along with the second one) is the one that helped to drop the length to below 1024. First we know that we can construct ```/``` and ```*```  by ```'/' = '-' xor "\x02"``` and ```'*' = '.' xor "\x04"```. A naive attempt is to combine to yield 

<center>'/*' = '-.'  <b>xor</b> "\x02\x04" = '-.' <b>xor</b> '24' <b>xor</b> '00'</center>

, but notice that the number of length of characters required to construct this is the same! Here, a big observation is that we can have 

<center>'/*' = '-.' <b>xor</b> '24' <b>xor</b> '00' = <u>'-4'</u> <b>xor</b> <u>'2.'</u> <b>xor</b> '00'</center>

Since we can use a long string for the xor, provided that we have a '00' to restrict the length of the final output of the xor to 2, we can get 2. by finding a floating point number ```2.???????E+???```, so we have 

<center>'/*' = '-4' <b>xor</b> '<b>2.</b><i>whateverE+whatever</i>' <b>xor</b> '00'</center>

And constructing -4 and a floating point number starting with 2. take much less space than the individual numbers 2,4 and the character ```-``` and ```.```. The final payload has length 928. On a high level, it is ```'ExEc'('/*h')```. In full, the payload are as follows (for those who are too lazy to run the python script themselves):

```((((([]^[[]]).([]^[]))**(([]^[[]]).([]^[]).([]^[])).([]^[]))[([]^[[]]).([]^[])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])]).((((([]^[[]]).([]^[])-([]^[[]]))**(([]^[[]]).([]^[]).([]^[]).([]^[])).([]^[]))[([]^[])])^(([]^[[]]).([]^[]))).(((([]^[[]]).([]^[]))**(([]^[[]]).([]^[]).([]^[])).([]^[]))[([]^[[]]).([]^[])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])]).((((([]^[[]]).([]^[])-([]^[[]]))**(([]^[[]]).([]^[]).([]^[]).([]^[])).([]^[]))[([]^[[]])])^(((-([]^[[]])).([]^[]))[([]^[])])))((((-(([]^[[]]).([]^[])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]])-([]^[[]]))).([]^[]))^((((([]^[[]]).([]^[])-([]^[[]])))**(([]^[[]]).([]^[]).([]^[]))).([]^[]))^(([]^[]).([]^[]))).((((([]^[[]]).([]^[]))**(([]^[[]]).([]^[]).([]^[])).([]^[]))[([]^[[]])])^(((([]^[[]]).([]^[])-([]^[[]]))**(([]^[[]]).([]^[]).([]^[]).([]^[])).([]^[]))[([]^[[]]).([]^[[]])^(([]^[[]]).([]^[])-([]^[[]]))])))```

which do give us the flag as desired.

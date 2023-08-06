
# SimpleTextProgressBar - A simple progress bar for simple projects  
This Text Progress Bar is made for projects that don't need great, big, confusing, etc. progress bars. It's code is only 3 KB, and It provides any progress bar relative size, with any relative value, with any prefix before the Progress Bar. 

## How to Install?  
    pip install simpletextprogressbar  
Or use [the .whl provided on GitHub](https://github.com/Inky1003/SimpleTextProgressBar/releases)

## How to use?  
Just  
  

    import simpletextprogressbar  

  
This imports the Progress Bar into your code  
  

    simpletextprogressbar.set_progress_bar()  

  
This function sends a unfinished line to the console.  
  

    simpletextprogressbar.change_position(position, size, optional_prefix, writeTheSameLineWhenFinished)  

  
This function sets a new progress bar in the relative position from the relative size, and also prints a text before the progress bar, If specified.  

## Examples
Imagine a example file:

    import time  
    import simpletextprogressbar  
    simpletextprogressbar.set_progress_bar()
    for x in range(10):  
            simpletextprogressbar.change_position(x+1, 10, "Filling 10% in 500 ms")  
            time.sleep(0.5)

  It Will return this:
![Filling 10% each 500 ms](https://i.imgur.com/4JTkGyp.gif)

## What changed?  
  
### 1.1.2  
  
- Added argument "writeTheSameLineWhenFinished", as a solution for writing after the line when the progressbar is at the same position as the size.
- Bug fixings
  
### 1.1.1  
  
- Bug fixing (not released, as I had the idea for 1.1.2)  
  
### 1.1.0  
  
- Initial release  
  
## Bug Fixing or Suggestions
  
If you find any bugs or want anything to be on the code, you are encouraged to use GitHub to tell me :)
  
Enjoy! 😉
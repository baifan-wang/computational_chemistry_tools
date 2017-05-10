# computational_chemistry_tools
[terminal_plot.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/terminal_plot.py): Python script for text-based plotting data in terminal, useful for ssh login. 

Sometimes people can only connect to remote server via ssh. To check the data generated on the remote server, one has to download these data. terminal_plot can directly display these data on the terminal to check whether is necessary to download these for further analysis.

Usage: ./terminal_plot.py data.dat data_column 
"data_column" specify which column data to plot(normally the first column (column 0) is used as x values, the second column (column 1) is the first y values).
![image](https://raw.githubusercontent.com/baifan-wang/computational_chemistry_tools/master/image/terminal_plot.png)

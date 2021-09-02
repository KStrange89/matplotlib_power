# Cancer Treatments

I was given data from a pharmaceutical company involving different cancer treatments on mice. I was tasked with comparing the effectiveness of different drug regimens. 

I used Pandas, MatPlotLib, SciPy, and numpy to complete this task.

I created a summary statistics table to compare the tumor volumes in each drug regimen.

I created bar graphs to compare the number of treatments for each drug regimen.

I used pie charts to view the distribution of male and female mice.

I used a line plot to look at the progress of one specific mouse, then I used multiple lines on one plot to compare the trends of four of the drug regimens-Capomulin, Ramicane, Ceftamin, and Infubinol.

I used a scatter plot to compare the average mouse weight and average tumor volume of all mice on the Capomulin regimen. I then used linregress to find the line of best fit. 

I also used box plots to compare the effectiveness of each treatment.

![alt text](https://github.com/KStrange89/matplotlib/blob/main/picture.png)

## Key Findings

* Ramicane seem to be the best drug option
** It has a smallest mean and median tumor volume
** It has the smallest variance and standard deviation in tumor volume

* Capolmulin seems to be the second best option
** It still has a success rate which is more than the others can say. But it has a lower stats than Ramicane across the board with one exception: IQR. Which suggests that it MAY be more predictable. However, even with Ramicane's higher IQR, the lower max and min suggest that Ramicane is the way to go.

* Even though Ceftamin and Infubinol have relatively small tumor volumes compared to the other regimens we did not look at in depth, they performed extremely poorly
** Both drugs had an increase in average tumor volume over time. 

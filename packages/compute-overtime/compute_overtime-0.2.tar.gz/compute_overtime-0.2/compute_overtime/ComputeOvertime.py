import pandas as pd
from datetime import datetime
from datetime import timedelta

class OverTimeCompute(object):
    """
    Overtime computation class for calculating the total hours of 
    overtime accumulated over a certain period of time.

    Attributes:
    lunch_length (int) - representing the length of allowable lunch break
    time_format (datetime) - representing the format in which the working 
                            hours are inputted (i.e. the start and finish time)
    date_date (datetime) - representing the format in which the 
                           working dates are inputted
    file - representing the csv timesheet
    """
    
    def __init__(self,lunch_length,time_format,date_format, file):
        """
        Attributes Initialisation
        """
        self.lunch_length = lunch_length                      
        self.time_format = time_format                            
        self.date_format = date_format  
        self.file = file


    def timesheet(self):
        """
        Loads and returns the csv timesheet as a dataframe
        """
        return pd.read_csv(self.file)
    

    def clean_data(self):
        """
        Checks and corrects any mistyped working dates and times
        """
        df = self.timesheet()
        
        starttime = [self.validateTime(time) for time in df.Start]
        endtime = [self.validateTime(time) for time in df.Finish]
        date = [self.validateDate(date) for date in df.Date]
        
        df.Start = starttime
        df.Finish = endtime
        df.Date = date
        
        return df
    
    
    def extract_weekday(self):
        """ 
        Extracts and creates a column for the day of 
        the week of each date
        """
        df = self.clean_data()
        day_weeks = []                      
        
        for i in range(len(df)):
            date = df.Date[i]
            day_weeks.append(datetime.strptime(str(date), 
                                self.date_format).strftime('%A'))
            
        df["Week_Day"] = day_weeks
        
        df.to_csv("timesheet.csv", index=False)
        
        return df 
    
    
    def isTimeFormat(self, worktime):
        """
        Validates the start and finish time format
        """
        try:
            datetime.strptime(str(worktime), self.time_format)
            return True
        except ValueError:
            return False


    def isDateFormat(self, date):
        """
        Validates the format of the dates
        """
        try:
            datetime.strptime(str(date), 
                              self.date_format).strftime("%d/%m/%Y")
            return True
        except ValueError:
            return False
        
        
    def validateTime(self, time):
        """
        Checks that the time format is correct. If incorrect, 
        requests user to re-enter the time
        """
        if self.isTimeFormat(time):
            return time
        else:
            new_time = input("Time format '{}' is incorrect."
                " Enter correct time ({}): ".format(time, 
                                     self.time_format))
            return new_time       
                
                
    def validateDate(self, date):
        """
        Checks that the date format is correct. If incorrect, 
        requests user to re-enter the date
        """
        if self.isDateFormat(date):
            return date
        else:
            new_date = input("Date format '{}' is incorrect."
                " Enter correct date ({}): ".format(date, 
                                     self.date_format))
            return new_date                                               


    def work_duration(self, td):
        """
        Converts the difference between the start and finish times
        into hours and minutes.
        """
        return (td.seconds//3600, (td.seconds//60)%60)           
#        
#    
    def dailyOvertime(self, timeMinusLunch):
        """
        Computes the daily overtime
        
        Args:
            timeMinusLunch = total hours worked excluding lunch time
            
        Assumption:
            This function assumes an 8-hour day shift
        """
        if self.work_duration(timeMinusLunch)[0] < \
        self.work_duration(timedelta(hours=8))[0]:
            overtime = timedelta(0)
        else:
            overtime = timeMinusLunch - timedelta(hours=8)                     
        
        return overtime


    def totalOvertimeCompute(self):
        """
        Computes the total overtime for the duration of work
        
        Returns:
            - total hours and minutes worked
            - total overtime hours and minutes
        """
        df = self.extract_weekday()
          
        total_overtime = {"Hours": 0, "Minutes": 0}     
        total_work_time = {"Hours": 0, "Minutes": 0}

        for i in range(len(df.Start)):            
            starttime = df.Start[i]
            endtime = df.Finish[i]
                
            worktime_plus_lunch = datetime.strptime(str(endtime),
                                self.time_format) - datetime.\
                            strptime(str(starttime), self.time_format)
            
            worktime_minus_lunch = worktime_plus_lunch -\
                                timedelta(minutes=self.lunch_length)
             
            overtime = self.dailyOvertime(worktime_minus_lunch)

            # Compute the total work time
            total_work_time["Hours"] += \
                    self.work_duration(worktime_minus_lunch)[0]            
            total_work_time["Minutes"] += \
                    self.work_duration(worktime_minus_lunch)[1]          
        
            # Compute the overtime hours worked
            total_overtime["Hours"] += self.work_duration(overtime)[0]            
            total_overtime["Minutes"] += self.work_duration(overtime)[1]       


        # Converts the total work time minutes to hours if minutes 
        # is more than 60 minutes
        if total_work_time["Minutes"] >= 60:                                        
            total_work_time["Hours"] += int(total_work_time["Minutes"] / 60)        
            total_work_time["Minutes"] = total_work_time["Minutes"] % 60            

        # Converts the total overtime minutes to hours if minutes 
        # is more than 60 minutes
        if total_overtime["Minutes"] >= 60:                                        
            total_overtime["Hours"] += int(total_overtime["Minutes"] / 60)        
            total_overtime["Minutes"] = total_overtime["Minutes"] % 60 
                        
        overtime_hours = total_overtime["Hours"]
        overtime_min = total_overtime["Minutes"]
        
        worktime_hours = total_work_time["Hours"]
        worktime_min = total_work_time["Minutes"]
        
        return worktime_hours, worktime_min, overtime_hours,overtime_min
        
        
    
"""
package:          htpbs
file:             bar.py
Author:           Jose Ortiz <jortizcocs@gmail.com>
Date Created:     04/09/2020
Last Modified:    04/10/2020
Licence:          MIT (see LICENSE.txt)

This script belongs to the htpbs package and is internally imported
by the file progressbars.py in the same package. It also can be imported
directly.

This scripts doesn't need imports from external packages.

"""


class Bar:
    """
        A class used to represent an single progress bar
    """

    def __init__(self, index=0, max_progress=100, prefix='', formatting='', suffix='',
                 num_decimals=2, length=10, fill='█', visible=True):
        """
        Class constructor
        :param index:
           If this bar belongs to a group of bars, the index define the position of this bar in
           screen relative to other bars. By default is set to 0.
        :param max_progress:
           The total max value allowed in progress. By default is set to 100.
           Note that if you are using for loops to increase the progress of
           the bar, and the max_total = 100, you need to set the range to range(101).
           Otherwise, the progress will stop at 99% if range(100)
        :param prefix:
           The str before the bar (i,e the name of the progress bar)
        :param formatting:
           The formatting used to format dynamic text (i.e "bar {0}".format(i) )
        :param suffix:
           The str suffix show after tha table
        :param num_decimals:
           The number of decimals that the table will show in the progress
        :param length:
           The length of the table.
        :param fill:
           Bar fill character
        """
        self.value = 0
        self.index = index
        self.max_progress = max_progress
        self.prefix = prefix
        self.format = formatting
        self.suffix = suffix
        self.decimals = num_decimals
        self.length = length
        self.fill = fill
        self.work_time = 0.0
        self.percent = "0.00"
        self.filled_length = 0
        self._visible = visible
        self._bar = None

    def bar(self):
        """"
        Creates a progress bar given all the parameters set in the class constructor
        :return: the string representation of the bar
        """

        value = self.value
        if self.prefix == '':
            self.prefix = "bar" + str(self.index) + self.format
        self.percent = ("{0:." + str(self.decimals) + "f}").format(100 * (value / float(self.max_progress)))
        self.filled_length = int(self.length * value // self.max_progress)
        self._bar = self.fill * self.filled_length + '-' * (self.length - self.filled_length)
        if value >= self.max_progress:
            self.suffix = "completed"
            self.percent = "100"
            self.filled_length = int(self.length * 100 // self.max_progress)
            self._bar = self.fill * self.filled_length + '-' * (self.length - self.filled_length)
        return '%s |%s| %s%% %s' % (self.prefix, self._bar, self.percent, self.suffix)

    def update(self, value):
        """
        Sets a new value in the progress bar
        IMPORTANT: bar() must be called again to see this new value represented in the progress bar
        :param value: the value to be updated
        :return: VOID
        """
        self.value = value

    def reset(self, value=0):
        """
        Resets the progress bar to zero. So, next time bar() is called it will start at progress zero
        :param value: (optional) the new value to be reset. Default is 0.
        :return: VOID
        """
        self.update(value)

    def hidden(self):
        """
        Hides the bar in screen.
        :return: VOID
        """
        self._visible = False

    def visible(self):
        """
        The bar is visible in screen. This is the default status of the bar.
        :return: VOID
        """
        self._visible = True

    def is_visible(self):
        """

        :return: is hidden return False. Otherwise, return True
        """
        return self._visible

    def reset_index(self, index):
        """
        Reset the index of the table.
        Useful when progress bar has completed work,
        and needs to start over again doing a different work
        :param index: the new index to be reset
        :return: VOID
        """
        self.index = index
        self.visible()
        self.reset()  # reset also the progress to 0

    def is_progress_completed(self):
        f_percent = float(self.percent)
        return f_percent >= 100



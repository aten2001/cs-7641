import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy as np



class plot_helper:
    def __init__(self):
        self.save_path= './output/'
        
    
    def plot_validation_curve(self, param_range, train_mean, train_std, test_mean, test_std, complexity_mean, complexity_std,
                              fit_time_mean, fit_time_std, predict_time_mean, predict_time_std, rev_axis, param_name, 
                              learner_name, save_file_name, complexity_name = '', plot_timing_bands=False):
        
        # plot
        plt.cla()    
        plt.clf()
        
        host = host_subplot(111, axes_class=AA.Axes)
        plt.subplots_adjust(right=0.75)
        
        par1 = host.twinx()
        par2 = host.twinx()
        
        offset = 60
        new_fixed_axis = par2.get_grid_helper().new_fixed_axis
        par2.axis["right"] = new_fixed_axis(loc="right",
                                            axes=par2,
                                            offset=(offset, 0))
        
        par2.axis["right"].toggle(all=True)
        
        host.set_xlabel(param_name)
        host.set_ylabel('Mean Squared Error')
        par1.set_ylabel(complexity_name)
        par2.set_ylabel('Time (Milliseconds)')
        
        p1, = host.plot(param_range, train_mean,
                        color='blue', marker='o',
                        markersize=5,
                        label='Training Error')
        
        host.fill_between(param_range,
                          train_mean + train_std,
                          train_mean - train_std,
                          alpha=0.15, color='blue')
        
        
        p2, = host.plot(param_range, test_mean,
                        color='green', marker='s',
                        markersize=5, linestyle='--',
                        label='Validation Error')
        
        host.fill_between(param_range,
                          test_mean + test_std,
                          test_mean - test_std,
                          alpha=0.15, color='green')
        
        if complexity_name != '':
            p3,  = par1.plot(param_range, complexity_mean,
                             color='red', marker='o',
                             markersize=5,
                             label=complexity_name)
            
            par1.fill_between(param_range,
                              complexity_mean + complexity_std,
                              complexity_mean - complexity_std,
                              alpha=0.15, color='red')
        
        p4, = par2.plot(param_range, fit_time_mean,
                        color='gray', marker='3',
                        markersize=5,
                        label='Fit Time')
        
        if plot_timing_bands:
            par2.fill_between(param_range,
                              fit_time_mean + fit_time_std,
                              fit_time_mean - fit_time_std,
                              alpha=0.15, color='gray')
        
        p5, = par2.plot(param_range, predict_time_mean,
                        color='orange', marker='4',
                        markersize=5,
                        label='Predict Time')
        if plot_timing_bands:
            par2.fill_between(param_range,
                              predict_time_mean + predict_time_std,
                              predict_time_mean - predict_time_std,
                              alpha=0.15, color='orange')
        
        host.legend(loc='best', fancybox=True, framealpha=0.5)
        
        host.axis["left"].label.set_color(p1.get_color())
        host.axis["left"].label.set_color(p2.get_color())
        
        if complexity_name != '':
            par1.axis["right"].label.set_color(p3.get_color())
            
        par2.axis["right"].label.set_color(p4.get_color())
        par2.axis["right"].label.set_color(p5.get_color())
        
        plt.grid()
        
        if complexity_name == '':
            plt.title("%s: Training, Validation Error (left)\nand Timings (right) Versus %s" % (learner_name, param_name))
        
        else:
            plt.title("%s: Training, Validation Error (left)\nand %s/Timings (right) Versus %s" % (learner_name, complexity_name, param_name))
        
        if (rev_axis):
            host.invert_xaxis()
        
        fn = self.save_path + save_file_name + '_validation.png'
        plt.savefig(fn)
        

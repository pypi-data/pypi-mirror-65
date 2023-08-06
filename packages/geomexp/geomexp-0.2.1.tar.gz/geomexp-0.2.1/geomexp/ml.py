import os,time
from pkg_resources import resource_string, resource_listdir, resource_filename
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
from random import randint, shuffle
from psychopy.iohub import launchHubServer, EventConstants

# By default, ioHub will create Keyboard and Mouse devices and
# start monitoring for any events from these devices only.
def ml_exp():
	'''
    The function runs the Muller-Lyer experiment. This will be updated with
	other details regarding the set stimuls, how to change it and other
	experimental conditions to be used.


    Parameters
    ----------
	NONE

    Returns
    -------
	Data from the expeiment in the data folder.
    '''
	io=launchHubServer(psychopy_monitor_name='testMonitor')


	#user values
	#image location
	#im= '../images/ml/tests/exp/ml_exp_15.png'

	keyboard=io.devices.keyboard
	increment = 0 # initial value of scaling factor

	#range of the reference line
	s=80.0

	#value in the rating scale
	rate1=rate=rate2=0.0

	#range of the rating scale
	range=10.0

	#images location
	loc=resource_filename('geomexp','ml_exp_10.png').rstrip('ml_exp_10.png')+ 'images/ml/'


	#list of images
	files= resource_listdir('geomexp.images.ml', '')
	for im in files:
		if not '.png' in im:
			files.remove(im)
	shuffle(files)

	try:#try to get a previous parameters file
		expInfo = fromFile('lastParams.pickle')
	except:#if not there then use a default set
		expInfo = {
		'subject':'jwp',
		'gender':'M',
		'age':0,
		'hand_pref':'R'
		}

	dateStr=time.strftime("%d-%m-%Y-%R-%s")
	#present a dialogue to change params
	dlg = gui.DlgFromDict(expInfo, title='Psychophysical Experiments', fixed=['dateStr'])
	if dlg.OK:
		toFile('lastParams.pickle', expInfo)#save params to file for next time
	else:
		pass
	try:# Create target Directory
		os.mkdir('data')
	except:
		pass
	#make a text file to save data
	fileName = expInfo['subject'] +'-ml.csv'
	file = open(os.getcwd()+'/data/'+fileName, 'a')#append mode

	file.write("%s,%s,%s,%s,%s\n" %(expInfo['subject'],expInfo['gender'],expInfo['age'],
		expInfo['hand_pref'],dateStr))

	win = visual.Window(
			size=[800, 800],
			units="pix",
			fullscr=1,
			color=[1, 1, 1],
			monitor="testMonitor",
			allowGUI=1
			)



	for im in files:
		label=im
		im=loc+im

		#image stimulus
#		try:

#		except:
#			print(' No image at '+im)

		img=visual.ImageStim(win=win,image=im, pos=[0,150],size=(400,400))
		#reference line
		#initial deviation
		dev=randint(-s,s)
		refline=visual.Line(win=win,start=(-99,-100),end=(77+dev,-100),lineColor='black',lineWidth=3)

		#the rating scale object
		ratingScale = visual.RatingScale(win=win, low=1, high=range ,pos=[0,-230],
			precision=10, scale='Length Scale', acceptText="Apply!!", showValue=0,
			lineColor="white", textColor="White", markerStart=(range-1.0)*(dev/(2.0*s)+0.5),
			marker='circle', markerColor='grey', size=0.75)

		while ratingScale.noResponse:
			img.draw()
			ratingScale.draw()
			rate=ratingScale.getRating()
			for event_io in keyboard.getEvents():
				if event_io.type == EventConstants.KEYBOARD_PRESS:
					if event_io.key == u'right':
						increment = 0.01 # move one step to the right
					elif event_io.key == u'left':
						increment = -0.01 # move one step to the left

				if event_io.type == EventConstants.KEYBOARD_RELEASE:
					increment = 0 # stop changing position


			ratingScale.markerPlacedAt += increment

			print ratingScale.markerPlacedAt,rate
			if rate!=rate1:
				refline=visual.Line(win=win,start=(-99-((2.0*(rate-1.0)
					/(range-1))-1)*(s/2.0),-100),end=(77+((2.0*(rate-1.0)
					/(range-1))-1)*(s/2.0),-100
					),lineColor='black',lineWidth=3)

			refline.draw()
			win.flip()
			rate1=rate
			#for prematurely closing program with 'q'
			if event.getKeys(['q']):
				win.close()
				io.quit()
				core.quit()
				file.close()
				#pause
			if event.getKeys(['escape']):
				win.winHandle.minimize() # minimise the PsychoPy window
				win.winHandle.set_fullscreen(False) # disable fullscreen
				win.flip() # redraw the (minimised) window
				raw_input("PAUSED!! Press Enter to continue experiment...")
				win.winHandle.maximize()
				win.winHandle.set_fullscreen(True)
				win.winHandle.activate()
				win.flip()


		#disparity
		disp=(2.0*(rate-1)/(range-1)-1)*s
		print(int(round(disp)))
		file.write("%d,%s\n" %(int(round(disp)),label))

	file.close()
	win.close()


# rating_subj = visual.RatingScale(win=win, name='rating_subj', pos=[1, 1], scale='Length',precision=100)

# positions = range(10)
# # random.shuffle(positions)
# # start = positions[0] + 1
# # rating_avrg = visual.RatingScale(win=win, name='rating_avrg', pos=[0.4, 0.4], scale='group',
# #     markerStart=str(start), minTime=0, maxTime=0.001)

# # rating_subj.draw()
# # win.flip()
# while rating_subj.noResponse:
#     rating_subj.draw()
#     a=rating_subj.getRating()
#     rating_avrg.draw()
#     win.flip()

# print(a)

# ratingScale = visual.RatingScale(win)
# item = [statement, question, image, movie]
# while ratingScale.noResponse:
#     item.draw()
#     ratingScale.draw()
#     win.flip()
# rating = ratingScale.getRating()
# decisionTime = ratingScale.getRT()
# choiceHistory = ratingScale.getHistory()
# print(rating)

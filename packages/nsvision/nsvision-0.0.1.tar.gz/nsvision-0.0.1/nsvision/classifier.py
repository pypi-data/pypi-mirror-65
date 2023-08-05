import os 
from shutil import copy2
from random import sample
def check_ratio_sum(ratio):
	"""
	Check the given ratio is valid or not. Sum of ratio should be 100
	"""

	train_ratio = int(ratio[0])
	val_ratio = int(ratio[1])
	test_ratio = int(ratio[2])
	qa_ratio = int(ratio[3])
	total = train_ratio + test_ratio + val_ratio + qa_ratio
	if total != 100:
		raise ValueError("Sum of all the input ratio should be equal to 100 ")
	return train_ratio, val_ratio, test_ratio, qa_ratio

def image_frequency(num,ratio):
	"""
	Find the frequency per class
	Parameter
	---------
	num: Total number of images
	ratio: split ratio
	"""
	ratio = ratio/100
	return round( num * ratio, 0 )


def split_image_data(data_dir,ratio,generate_labels_txt=False):
	"""
	Divides image data required for classification according to Train, Test, Validation and QA

	Parameters:
	data_dir:  path to image data folder
	ratio: Tuple ratio
	generate_labels_txt: set to True if you want to generate labels.txt for the classes.
		Default(False)
	"""
	if not isinstance(ratio, tuple):
		raise TypeError(f"ratio should be tuple of (train,val,test,qa) but got {ratio} of type {type(ratio)} instead")

	if len(ratio) != 4:
		raise ValueError(f"required ratio to be of length 4 but got length {len(ratio)} instead")
	#ratio 
	train_ratio, val_ratio, test_ratio, qa_ratio = check_ratio_sum(ratio)

	#making new_dir to save divided data
	folder_name = os.path.splitext(os.path.basename(data_dir))[0]
	new_folder = folder_name + "_classified_data"
	model_data_dir = os.path.join(os.path.dirname(data_dir),new_folder)
	os.makedirs(model_data_dir,exist_ok = True)

	os.makedirs(os.path.join(model_data_dir,"train"),exist_ok = True)
	os.makedirs(os.path.join(model_data_dir,"test"),exist_ok = True)
	os.makedirs(os.path.join(model_data_dir,"val"),exist_ok = True)
	os.makedirs(os.path.join(model_data_dir,"qa"),exist_ok = True)

	folder_names = ['train','val','test','qa']

	#dividing the data into given ratio
	classes_list = os.listdir(data_dir)

	print("Total number of classes",len(classes_list))
	try:
		for class_name in classes_list:
			class_path = os.path.join(data_dir,class_name)
			
			class_images = os.listdir(class_path)
			
			total_class_images = len(class_images)

			total_train_images = image_frequency(total_class_images,train_ratio)
			total_val_images = image_frequency(total_class_images,val_ratio)
			total_test_images = image_frequency(total_class_images,test_ratio)
			total_qa_images = image_frequency(total_class_images,qa_ratio)

			ratio_list = [total_train_images,total_val_images,total_test_images,total_qa_images]

			class_images_new = class_images
			class_images_new = sample(class_images_new,len(class_images_new))

			div1 = total_train_images
			div2 = div1 + total_val_images
			div3 = div2 + total_test_images
			print(f"\nData divided for class {class_name} as follows:-",f"Train: {div1}",f"Validation: {div2 - div1}", f"Test: {div3 -div2}",f"QA: {total_class_images - div3}\n",sep='\n')
			train_list = class_images_new[:int(div1)]
			val_list = class_images_new[int(div1):int(div2)]
			test_list = class_images_new[int(div2):int(div3)]
			qa_list = class_images_new[int(div3):]
			split_lst = [train_list,val_list,test_list,qa_list]
			for i,j in zip(folder_names,split_lst):
				for img in j:
					src_path = os.path.join(class_path,img)
					dst_path = os.path.join(os.path.join(model_data_dir,i),class_name)
					os.makedirs(dst_path,exist_ok=True)
					copy2(src_path,dst_path)
		if generate_labels_txt:
			print("Generating labels.txt")
			with open(os.path.join(os.path.dirname(data_dir),'labels.txt'),'w') as labels_file:
				labels_file.write("\n".join(classes_list))
	except:
		raise Exception("Failed to split data please check folder structure or check your OS Permission")
	print("Splitting completed",f"Splitted data is stored at {model_data_dir}",sep='\n')
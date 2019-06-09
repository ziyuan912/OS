# DIP final package

All : skincolor morph shape template_mathing cleaning
skincolor :
	 @echo "perform skincolor segmentation method:"
	 @echo "running the program, usage: python skincolor.py image_file"
	 @echo "temperary output: output1.jpeg"
	 @python skincolor.py ../sample/test.jpeg

morph :
	 @echo "perform noise removal and morphological processing:"
	 @echo "running the program, usage: python morph.py"
	 @echo "temperary output: output2.jpeg"
	 @python morph.py

shape:
	 @echo "perform eular number method:"
	 @echo "running the program, usage: python shape.py"
	 @echo "temperary output: output3.jpeg"
	 @python shape.py

template_mathing :
	 @echo "perform template matching:"
	 @echo "running the program, usage: python template_matching.py"
	 @echo "final output: output.jpeg"
	 @python template_matching.py

cleaning:
	@echo "cleaning temperary output:"
	@rm output1.jpeg
	@rm output2.jpeg
	@rm output3.jpeg
	@echo "clening successfully"

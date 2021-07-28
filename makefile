#
#Requires existing installation of java, ideally OpenJDK version 11
#  


#links
citygmltools = https://github.com/citygml4j/citygml-tools/releases/download/v1.4.2/citygml-tools-1.4.2.zip



all: linux
.PHONY: linux citygml toolsfolder javacheck java clean

linux: clean citygml python java


toolsfolder:
	@-( \
		([ -d "tools" ] || mkdir tools); \
	)

#Install CityGML Tools into tools folder and unpack 
#https://github.com/citygml4j/citygml-tools/
citygml: toolsfolder java
	@-( \
		cd tools; \
		wget -O gmltools.zip $(citygmltools); \
		mkdir citygmltools; \
		unzip gmltools.zip -d citygmltools; \
		rm gmltools.zip; \
		cd ..; \
	)

java: toolsfolder
	@-( \
		cd tools; \
		wget -O java.tar.gz https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_linux-x64_bin.tar.gz; \
		tar -xf java.tar.gz; \
		echo "Add to .bashrc file following line"; \
		jpath=`readlink -f jdk-16.0.2/`; \
		echo "export PATH=$$jpath/bin:\$$PATH"; \
		export PATH=$$jpath/bin:\$$PATH; \
		echo "export JAVA_HOME=$$jpath/"; \
		export JAVA_HOME=$$jpath/; \
		rm java.tar.gz; \
		cd ..; \
	)


#environments
environment:
	@-( \
		echo "checking linux python environment"; \
		\
		virtualenv 2>&1 >/dev/null; \
		([ "$$?" != "127" ] && echo "virtualenv installed") \
		|| sudo apt install virtualenv; \
	)


python: environment
	@-( \
		echo "creating python environment"; \
		virtualenv --python=python3 env; \
		. ./env/bin/activate; \
		\
		echo "installing requirements"; \
		pip install -r requirements.txt; \
	)



javacheck:
	@-( \
		java -version 2>&1 >/dev/null | grep "java version\|openjdk version"; \
	)


clean:
	@-rm -rf tools

#
#Requires existing installation of java, ideally OpenJDK version 11
#  


#links
citygmltools = https://github.com/citygml4j/citygml-tools/releases/download/v1.4.2/citygml-tools-1.4.2.zip



all: linux
.PHONY: linux citygml toolsfolder javacheck clean

linux: clean citygml


toolsfolder:
	@-( \
		([ -d "tools" ] || mkdir tools); \
	)

#Install CityGML Tools into tools folder and unpack 
#https://github.com/citygml4j/citygml-tools/
citygml: toolsfolder javacheck
	@-( \
		cd tools; \
		wget -O gmltools.zip $(citygmltools); \
		mkdir citygmltools; \
		unzip gmltools.zip -d citygmltools; \
		rm gmltools.zip; \
		cd ..; \
	)

javacheck:
	@-( \
		java -version 2>&1 >/dev/null | grep "java version\|openjdk version"; \
	)


clean:
	@-rm -rf tools

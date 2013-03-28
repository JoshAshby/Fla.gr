BOOTSTRAP_LESS = ./interface/resources/less/bootstrap/bootstrap.less
BOOTSTRAP_ADMIN_LESS = ./interface/resources/less/bootstrap/adminBootstrap.less
BOOTSTRAP_RESPONSIVE_LESS = ./interface/resources/less/bootstrap/responsive.less
FONTAWESOME_LESS = ./interface/resources/less/fontawesome/font-awesome.less
CUSTOM_LESS = ./interface/resources/less/custom_styles.less
COFFEE_DIR = ./interface/resources/cs/
CHECK=✔
DOCS_DIR = ./docs/

flagr: bootstrap less coffee templates
	@echo "You should link interface/resources to your servers /static/"
	@echo "In other words, interface/resources should be accessible from localhost/static"

bootstrap:
	@echo "Compiling Twitter Bootstrap..."
	mkdir -p interface/resources/css/bootstrap
	./node_modules/.bin/recess --compile ${BOOTSTRAP_LESS} > interface/resources/css/bootstrap/bootstrap.css
	./node_modules/.bin/recess --compress ${BOOTSTRAP_LESS} > interface/resources/css/bootstrap/bootstrap.min.css
	./node_modules/.bin/recess --compile ${BOOTSTRAP_ADMIN_LESS} > interface/resources/css/bootstrap/adminBootstrap.css
	./node_modules/.bin/recess --compress ${BOOTSTRAP_ADMIN_LESS} > interface/resources/css/bootstrap/adminBootstrap.min.css
	./node_modules/.bin/recess --compile ${BOOTSTRAP_RESPONSIVE_LESS} > interface/resources/css/bootstrap/bootstrap-responsive.css
	./node_modules/.bin/recess --compress ${BOOTSTRAP_RESPONSIVE_LESS} > interface/resources/css/bootstrap/bootstrap-responsive.min.css
	@echo "Done ${CHECK}"
	@echo "Compiling Font-Awesome for Bootstrap..."
	mkdir -p interface/resources/css/fontawesome
	./node_modules/.bin/recess --compile ${FONTAWESOME_LESS} > interface/resources/css/fontawesome/fontawesome.css
	./node_modules/.bin/recess --compress ${FONTAWESOME_LESS} > interface/resources/css/fontawesome/fontawesome.min.css
	@echo "Done ${CHECK}"

less:
	@echo "Compiling custom LESS..."
	./node_modules/.bin/recess --compile ${CUSTOM_LESS} > interface/resources/css/custom_styles.css
	./node_modules/.bin/recess --compress ${CUSTOM_LESS} > interface/resources/css/custom_styles.css
	@echo "Done ${CHECK}"

coffee:
	@echo "Compiling CoffeeScript..."
	./node_modules/.bin/coffee --compile --output interface/resources/js/ ${COFFEE_DIR}
	@echo "Done ${CHECK}"

templates:
	@echo "Compiling Cheetah templates..."
	cheetah compile -R --idir interface/templates/ --odir flagr_core/views/
	@echo "Done ${CHECK}"

htmldocs:
	@echo "Compiling docs as HTML into docs/build/html"
	$(MAKE) -C ${DOCS_DIR} html
	@echo "Done ${CHECK}"

clean:
	@echo "Cleaning up a few directories I made..."
	rm -rf interface/resources/css/bootstrap
	rm -rf interface/resources/css/fontawesome
	rm -rf flagr_core/views
	rm -rf docs/build
	@echo "Done ${CHECK}"


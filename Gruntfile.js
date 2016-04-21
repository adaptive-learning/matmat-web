module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dist: {
                options: {
                    loadPath: 'bower_components/foundation/scss'
                },
                files: {
                    'static-source/css/foundation.css': 'static-source/css/foundation.custom.scss'
                }
            }
        },
        concat: {
            libs: {
                src: [
                    'bower_components/foundation/js/vendor/jquery.js',
                    'bower_components/angular/angular.min.js',
                    'bower_components/angular-cookies/angular-cookies.min.js',
                    'bower_components/angular-route/angular-route.min.js',
                    'bower_components/angular-foundation/mm-foundation-tpls.min.js',
                    'bower_components/jsTimezoneDetect/jstz.min.js',
                    'bower_components/proso-apps-js/proso-apps-services.js',
                    'bower_components/foundation/js/vendor/modernizr.js',
                    'bower_components/foundation/js/vendor/fastclick.js',
                    'bower_components/foundation/js/foundation.min.js',
                    'bower_components/foundation/js/foundation/foundation.clearing.js',
                    'bower_components/foundation/js/foundation/foundation.reveal.js'
                ],
                dest: 'static/libs.min.js'
            },
            dist: {
                src: ['static-source/js/*.js', 'static-source/ng-templates/templates.js'],
                dest: 'static/matmat.js'
            }
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %>-libs <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                src: 'static/matmat.js',
                dest: 'static/matmat.min.js'
            }
        },
        jshint: {
            files: ['static-source/js/*.js']
        },
        watch: {
            files: ['static-source/js/*.js', "static-source/css/*.css", "static-source/ng-templates/*.html"],
            tasks: ['jshint', 'ngtemplates', 'concat:dist', 'uglify:build', "cssmin"]
        },
        cssmin: {
            target: {
                files: {
                    'static/matmat.min.css': [
                        "bower_components/foundation/css/normalize.css",
                        "static-source/css/foundation.css",
                        'static-source/css/*.css'
                    ]
                }
            }
        },
        ngtemplates:  {
            matmat: {
                src: 'static-source/ng-templates/*.html',
                dest: 'static-source/ng-templates/templates.js'
            }
        },
        copy: {
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-sass');

    grunt.registerTask('foundation', ['sass']);
    grunt.registerTask('default', ['jshint', 'foundation', 'ngtemplates', 'concat', 'uglify:build', 'cssmin']);
};
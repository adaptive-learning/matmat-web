module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            js: {
                src: [
                    'static/foundation/js/vendor/modernizr.js',
                    "static/foundation/js/vendor/jquery.js",
                    'static/underscore-min.js',
                    'static/angular/angular.min.js',
                    'static/angular/angular-cookies.min.js',
                    'static/angular/angular-animate.min.js',
                    'static/scripts.js',
                    'static/core/scripts.js',
                    'static/angular/mm-foundation-tpls.min.js',
                    'static/core/angular.js',
                    'static/core/feedback.js',
                    'static/my_skills.js',
                    "static/graphics/wizard/wizard.js",
                    "static/foundation/js/foundation.min.js",
                    "static/simulators/loader.js",
                    "static/simulators/directives.js",
                    "static/simulators/keyboard-wizard.js",
                    "static/simulators/roller-wizard.js",
                    "static/simulators/roller-wizard.js",
                    "static/simulators/counter-wizard.js",
                    "static/simulators/**/controller.js",
                    "static/dist/templates.js"
                ],
                dest: 'static/dist/matmat.js'
            }
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %>-libs <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                src: 'static/dist/matmat.js',
                dest: 'static/dist/matmat.min.js'
            }
        },
        cssmin: {
            target: {
                files: {
                    'static/dist/wizard/matmat.min.css': [
                        "static/foundation/css/normalize.css",
                        "static/foundation/css/foundation.min.css",
                        "static/foundation/icons/foundation-icons.css",
                        "static/core/*.css",
                        "static/graphics/wizard/*.css"
                    ],
                    'static/dist/plain/matmat.min.css': [
                        "static/foundation/css/normalize.css",
                        "static/foundation/css/foundation.min.css",
                        "static/foundation/icons/foundation-icons.css",
                        "static/core/*.css",
                        "static/graphics/plain/*.css"
                    ]
                }
            }
        },
        ngtemplates:  {
            matmat: {
                cwd: "static",
                src: ['simulators/**/*.html', "graphics/wizard/wizard.html"],
                dest: 'static/dist/templates.js'
            }
        },
        copy: {
            iconswi: {
                cwd: 'static/foundation/icons',  // set working folder / root to copy
                src: '**/*',           // copy all files and subfolders
                dest: 'static/dist/wizard',    // destination folder
                expand: true           // required when using cwd
            },
            iconspl: {
                cwd: 'static/foundation/icons',  // set working folder / root to copy
                src: '**/*',           // copy all files and subfolders
                dest: 'static/dist/plain',    // destination folder
                expand: true           // required when using cwd
            },
            plain: {
                cwd: 'static/graphics/plain',  // set working folder / root to copy
                src: '**/*',           // copy all files and subfolders
                dest: 'static/dist/plain',    // destination folder
                expand: true           // required when using cwd
            },
            wizard: {
                cwd: 'static/graphics/wizard',  // set working folder / root to copy
                src: '**/*',           // copy all files and subfolders
                dest: 'static/dist/wizard',    // destination folder
                expand: true           // required when using cwd
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ["cssmin", "copy", "ngtemplates", "concat", "uglify"]);
};
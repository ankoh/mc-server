/*jslint node: true, indent: 2 */
'use strict';
module.exports = function (grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg     : grunt.file.readJSON('package.json'),
    jshint  : {
      all     : ['package.json', 'Gruntfile.js', 'index.js', 'routes/**/*.js', 'lib/**/*.js', 'specs/**/*.js']
    },
    mochaTest: {
      specs: {
          options: {
            ui: 'bdd',
            reporter: 'spec',
            require: './specs/helpers/chai'
          },
          src: ['specs/**/*.spec.js']
        }
      }
    });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-mocha-test');
  grunt.loadNpmTasks('grunt-serve');

  // Default task(s).
  grunt.registerTask('default', [
    'jshint',
    'mochaTest'
  ]);

};


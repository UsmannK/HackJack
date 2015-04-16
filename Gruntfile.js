module.exports = function(grunt) {
    grunt.initConfig({
        sass: {
            dist: {
                files: {
                    // 'assets/stylesheets/bootstrap.css': 'assets/bootstrap/stylesheets/bootstrap.scss',
                    'static/base.css': 'sass/base.scss'
                }
            }
        },
        autoprefixer: {
            single_file: {
                src: 'static/base.css',
                dest: 'static/base.css'
            }
        },
        watch: {
            source: {
                files: ['sass/*.scss'],
                tasks: ['sass', 'autoprefixer'],
                options: {
                    livereload: true, // needed to run LiveReload
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-livereload');
    grunt.loadNpmTasks('grunt-autoprefixer');

    grunt.registerTask('default', ['sass', 'autoprefixer']);
};

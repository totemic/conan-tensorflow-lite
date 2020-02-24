import sys
from os import getcwd
from multiprocessing import cpu_count
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class TFLiteConan(ConanFile):
    # Basic info
    name = "tensorflow-lite"
    version = "2.1.0"
    repo_url = "https://github.com/tensorflow/tensorflow.git"

    # Other package details
    description = "https://www.tensorflow.org"
    license = "Apache-2.0"

    # Conan build process settings
    exports = ['01-fix-download-dependencies.patch']
    settings = "os", "arch", "compiler", "build_type"
    source_subfolder = "tensorflow"
    build_subfolder = "tensorflow/lite/tools/make"
    generators = "make"

    def build_requirements(self):
        pass

    def source(self):
        git = tools.Git(folder=self.source_subfolder)
        git.clone(self.repo_url)
        with tools.chdir(self.source_subfolder):
            self.run(f"git checkout -b v{self.version} tags/v{self.version}")
            tools.patch(patch_file="../01-fix-download-dependencies.patch")

    def build(self):
        with tools.chdir(self.source_subfolder):
            self.run(f"{self.build_subfolder}/download_dependencies.sh")
            self.run(f"{self.build_subfolder}/build_lib.sh")

    def package(self):
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.h", dst="include/tensorflow/lite", src="tensorflow/tensorflow/lite", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["tensorflow-lite", "pthread"]

from conans import ConanFile, tools

VERSION = "2.1.0"

class TFLiteConan(ConanFile):
    # Basic info
    name = "tensorflow-lite"
    version = VERSION
    scm = dict(type="git",
               url="https://github.com/tensorflow/tensorflow.git",
               revision=f"v{VERSION}")

    # Other package details
    description = "https://www.tensorflow.org"
    license = "Apache-2.0"

    # Conan build process settings
    exports = ['01-fix-download-dependencies.patch']
    settings = "os", "arch", "compiler", "build_type"
    
    build_subfolder = "tensorflow/lite/tools/make"

    def requirements(self):
        self.requires('flatbuffers/1.11.0@google/stable')

    def source(self):
        tools.patch(patch_file="01-fix-download-dependencies.patch")
        self.run(f"{self.build_subfolder}/download_dependencies.sh")

    def build(self):
        if self.settings.arch == "armv8":
            self.run(f"{self.source_folder}/{self.build_subfolder}/build_aarch64_lib.sh")
        else:
            self.run(f"{self.source_folder}/{self.build_subfolder}/build_lib.sh")

    def package(self):
        self.copy(pattern="*/libtensorflow-lite.a", dst="lib", src=f"tensorflow/lite", keep_path=False)
        self.copy(pattern="*.h", dst="include/tensorflow/lite", src=f"tensorflow/lite", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["tensorflow-lite", "pthread"]

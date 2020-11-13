from conans import ConanFile, tools

VERSION = "2.5.0.post1"

class TFLiteConan(ConanFile):
    # Basic info
    name = "tensorflow-lite"
    version = VERSION
    scm = dict(type="git",
               url="https://github.com/tensorflow/tensorflow.git",
               revision=f"f394a768719a55b5c351ed1ecab2ec6f16f99dd4")

    # Other package details
    description = "https://www.tensorflow.org"
    license = "Apache-2.0"

    # Conan build process settings
    exports = ["01-fix-missing-sources.patch", "02-tar-instead-of-zip.patch"]
    settings = "os", "arch", "compiler", "build_type"

    build_subfolder = "tensorflow/lite/tools/make"

    def requirements(self):
        self.requires('flatbuffers/1.12.0@google/stable')

    def source(self):
        # tools.patch(patch_file="01-fix-missing-sources.patch")
        # tools.patch(patch_file="02-tar-instead-of-zip.patch")
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
        self.cpp_info.libs = ["tensorflow-lite", "stdc++"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["c", "m", "dl", "rt", "pthread"])

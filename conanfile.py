from os.path import join
from conans import AutoToolsBuildEnvironment, ConanFile, tools

VERSION = "2.5.0.post1"
BUILD_SUBFOLDER = "tensorflow/lite/tools/make"


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
    exports = ["01-tar-instead-of-zip.patch", "02-ignore-nnapi.patch"]
    settings = "os", "arch", "compiler", "build_type"

    # def system_requirements(self):
    #     installer = tools.SystemPackageTool()
    #     installer.install("make")

    def requirements(self):
        self.requires('flatbuffers/1.12.0@google/stable')

    def source(self):
        tools.patch(patch_file="01-tar-instead-of-zip.patch")
        tools.patch(patch_file="02-ignore-nnapi.patch")

        self.run(join(BUILD_SUBFOLDER, "download_dependencies.sh"))

    def build(self):
        build_folder = join(self.source_folder, BUILD_SUBFOLDER)
        is_aarch64 = self.settings.arch == "armv8"

        # Note: the only advantage of using scripts is that when building
        #  on aarch64 with low memory, building will be single-threaded

        # if is_aarch64:
        #     self.run(join(build_folder, "build_aarch64_lib.sh"))
        # else:
        #     self.run(join(build_folder, "build_lib.sh"))

        target_opt = "TARGET=aarch64" if is_aarch64 else ""
        env_vars = {'SCRIPT_DIR': build_folder, 'TENSORFLOW_DIR': self.source_folder}

        autotools = AutoToolsBuildEnvironment(self)
        with tools.chdir(self.source_folder):
            autotools.make(target=f"{target_opt} -f {build_folder}/Makefile micro", vars=env_vars)

    def package(self):
        self.copy(pattern="*/libtensorflow-lite.a", dst="lib", src=f"tensorflow/lite", keep_path=False)
        self.copy(pattern="*.h", dst="include/tensorflow/lite", src=f"tensorflow/lite", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["tensorflow-lite", "stdc++"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["c", "m", "dl", "rt", "pthread"])

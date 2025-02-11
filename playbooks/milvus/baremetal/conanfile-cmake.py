from conans import ConanFile, tools

class CmakeConan(ConanFile): 
  name = "cmake" 
  package_type = "application" 
  version = "%{ cmake_version }%"
  description = "CMake, the cross-platform, open-source build system." 
  homepage = "https://github.com/Kitware/CMake" 
  license = "BSD-3-Clause" 
  topics = ("build", "installer") 
  settings = "os", "arch" 

  def package(self): 
    self.copy("*") 

  def package_info(self): 
    self.cpp_info.libs = tools.collect_libs(self)
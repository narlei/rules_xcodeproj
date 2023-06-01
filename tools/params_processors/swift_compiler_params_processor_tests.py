"""Tests for swift_compiler_params_processor."""

import unittest

from tools.params_processors import swift_compiler_params_processor

class swift_compiler_params_processor_test(unittest.TestCase):
    def test_paths(self):
        def _parse_args(args):
            return iter([f"{arg}\n" for arg in args])

        self.assertEqual(
            swift_compiler_params_processor.process_args(
                [[
                    "swift_worker",
                    "swiftc",

                    # -fmodule-map-file
                    "-Xcc",
                    "-fmodule-map-file=/absolute/path",
                    "-Xcc",
                    "-fmodule-map-file=relative/path",
                    "-Xcc",
                    "-fmodule-map-file=.",

                    # -iquote
                    "-iquote/absolute/path",
                    "-iquote",
                    "/absolute/path",
                    "-iquote",
                    "/absolute/path",
                    "-iquoterelative/path",
                    "-iquote",
                    "relative/path",
                    "-iquote.",
                    "-iquote",
                    ".",

                    "-Xcc",
                    "-iquote/absolute/path",
                    "-Xcc",
                    "-iquote",
                    "-Xcc",
                    "/absolute/path",
                    "-Xcc",
                    "-iquote",
                    "-Xcc",
                    "/absolute/path",
                    "-Xcc",
                    "-iquoterelative/path",
                    "-Xcc",
                    "-iquote",
                    "-Xcc",
                    "relative/path",
                    "-Xcc",
                    "-iquote.",
                    "-Xcc",
                    "-iquote",
                    "-Xcc",
                    ".",

                    # -I
                    "-I/absolute/path",
                    "-I",
                    "/absolute/path",
                    "-Irelative/path",
                    "-I",
                    "relative/path",
                    "-I.",
                    "-I",
                    ".",

                    "-Xcc",
                    "-I/absolute/path",
                    "-Xcc",
                    "-I",
                    "-Xcc",
                    "/absolute/path",
                    "-Xcc",
                    "-Irelative/path",
                    "-Xcc",
                    "-I",
                    "-Xcc",
                    "relative/path",
                    "-Xcc",
                    "-I.",
                    "-Xcc",
                    "-I",
                    "-Xcc",
                    ".",

                    # -isystem
                    "-isystem/absolute/path",
                    "-isystem",
                    "/absolute/path",
                    "-isystemrelative/path",
                    "-isystem",
                    "relative/path",
                    "-isystem.",
                    "-isystem",
                    ".",

                    "-Xcc",
                    "-isystem/absolute/path",
                    "-Xcc",
                    "-isystem",
                    "-Xcc",
                    "/absolute/path",
                    "-Xcc",
                    "-isystemrelative/path",
                    "-Xcc",
                    "-isystem",
                    "-Xcc",
                    "relative/path",
                    "-Xcc",
                    "-isystem.",
                    "-Xcc",
                    "-isystem",
                    "-Xcc",
                    ".",
                ]],
                parse_args = _parse_args,
            ),
            [
                # -fmodule-map-file
                "-Xcc",
                "-fmodule-map-file=/absolute/path",
                "-Xcc",
                "'-fmodule-map-file=$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "'-fmodule-map-file=$(PROJECT_DIR)'",

                # -iquote
                "-iquote/absolute/path",
                "-iquote",
                "/absolute/path",
                "-iquote",
                "/absolute/path",
                "'-iquote$(PROJECT_DIR)/relative/path'",
                "-iquote",
                "'$(PROJECT_DIR)/relative/path'",
                "'-iquote$(PROJECT_DIR)'",
                "-iquote",
                "'$(PROJECT_DIR)'",

                "-Xcc",
                "-iquote/absolute/path",
                "-Xcc",
                "-iquote",
                "-Xcc",
                "/absolute/path",
                "-Xcc",
                "-iquote",
                "-Xcc",
                "/absolute/path",
                "-Xcc",
                "'-iquote$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "-iquote",
                "-Xcc",
                "'$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "'-iquote$(PROJECT_DIR)'",
                "-Xcc",
                "-iquote",
                "-Xcc",
                "'$(PROJECT_DIR)'",

                # -I
                "-Xcc",
                "-I/absolute/path",
                "-Xcc",
                "-I",
                "-Xcc",
                "/absolute/path",
                "-Xcc",
                "'-I$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "-I",
                "-Xcc",
                "'$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "'-I$(PROJECT_DIR)'",
                "-Xcc",
                "-I",
                "-Xcc",
                "'$(PROJECT_DIR)'",

                # -isystem
                "-isystem/absolute/path",
                "-isystem",
                "/absolute/path",
                "'-isystem$(PROJECT_DIR)/relative/path'",
                "-isystem",
                "'$(PROJECT_DIR)/relative/path'",
                "'-isystem$(PROJECT_DIR)'",
                "-isystem",
                "'$(PROJECT_DIR)'",

                "-Xcc",
                "-isystem/absolute/path",
                "-Xcc",
                "-isystem",
                "-Xcc",
                "/absolute/path",
                "-Xcc",
                "'-isystem$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "-isystem",
                "-Xcc",
                "'$(PROJECT_DIR)/relative/path'",
                "-Xcc",
                "'-isystem$(PROJECT_DIR)'",
                "-Xcc",
                "-isystem",
                "-Xcc",
                "'$(PROJECT_DIR)'",
            ],
        )

    def test_replacements(self):
        def _parse_args(args):
            return iter([f"{arg}\n" for arg in args])

        self.assertEqual(
            swift_compiler_params_processor.process_args(
                [[
                    "swift_worker",
                    "swiftc",
                    "-F__BAZEL_XCODE_DEVELOPER_DIR__/Hi",
                    "-I__BAZEL_XCODE_SDKROOT__/Yo",
                    "-I__BAZEL_XCODE_SOMETHING_/path",
                ]],
                parse_args = _parse_args,
            ),
            [
            ],
        )

    def test_skips(self):
        def _parse_args(args):
            return iter([f"{arg}\n" for arg in args])

        self.assertEqual(
            swift_compiler_params_processor.process_args(
                [[
                    "swift_worker",
                    "swiftc",
                    "-output-file-map",
                    "path",
                    "-passthrough",
                    "-debug-prefix-map",
                    "__BAZEL_XCODE_DEVELOPER_DIR__=DEVELOPER_DIR",
                    "-file-prefix-map",
                    "__BAZEL_XCODE_DEVELOPER_DIR__=DEVELOPER_DIR",
                    "-emit-module-path",
                    "path",
                    "-passthrough",
                    "-Xfrontend",
                    "-color-diagnostics",
                    "-Xfrontend",
                    "-import-underlying-module",
                    "-emit-object",
                    "-enable-batch-mode",
                    "-passthrough",
                    "-gline-tables-only",
                    "-sdk",
                    "something",
                    "-module-name",
                    "name",
                    "-passthrough",
                    "-I__BAZEL_XCODE_SOMETHING_/path",
                    "-num-threads",
                    "6",
                    "-passthrough",
                    "-Ibazel-out/...",
                    "-parse-as-library",
                    "-passthrough",
                    "-parse-as-library",
                    "-keep-me=something.swift",
                    "reject-me.swift",
                    "-target",
                    "ios",
                    "-Xcc",
                    "-weird",
                    "-Xcc",
                    "-a=bazel-out/hi",
                    "-Xwrapped-swift",
                    "-passthrough",
                ]],
                parse_args = _parse_args,
            ),
            [
                "-passthrough",
                "-passthrough",
                "-Xfrontend",
                "-import-underlying-module",
                "-passthrough",
                "-passthrough",
                "-passthrough",
                "-passthrough",
                "-keep-me=something.swift",
                "-Xcc",
                "-weird",
                "-Xcc",
                "-a=bazel-out/hi",
                "-passthrough",
            ],
        )

    def test_explicit_swift_module_map_file(self):
        def _parse_args(args):
            return iter([f"{arg}\n" for arg in args])

        self.assertEqual(
            swift_compiler_params_processor.process_args(
                [[
                    "swift_worker",
                    "swiftc",
                    "-explicit-swift-module-map-file",
                    "/Some/Path.json",
                    "-explicit-swift-module-map-file",
                    "relative/Path.json",
                    "-Xfrontend",
                    "-explicit-swift-module-map-file",
                    "-Xfrontend",
                    "/Some/Path.json",
                    "-Xfrontend",
                    "-explicit-swift-module-map-file",
                    "-Xfrontend",
                    "relative/Path.json",
                ]],
                parse_args = _parse_args,
            ),
            [],
        )

    def test_vfsoverlay(self):
        def _parse_args(args):
            return iter([f"{arg}\n" for arg in args])

        self.assertEqual(
            swift_compiler_params_processor.process_args(
                [[
                    "swift_worker",
                    "swiftc",
                    "-vfsoverlay",
                    "/Some/Path.yaml",
                    "-vfsoverlay",
                    "relative/Path.yaml",
                    "-Xfrontend",
                    "-vfsoverlay",
                    "-Xfrontend",
                    "/Some/Path.yaml",
                    "-Xfrontend",
                    "-vfsoverlay",
                    "-Xfrontend",
                    "relative/Path.yaml",
                    "-Xfrontend",
                    "-vfsoverlay/Some/Path.yaml",
                    "-Xfrontend",
                    "-vfsoverlayrelative/Path.yaml",
                    "-Xfrontend",
                    "-vfsoverlay=/Some/Path.yaml",
                    "-Xfrontend",
                    "-vfsoverlay=relative/Path.yaml",
                ]],
                parse_args = _parse_args,
            ),
            [],
        )

    def test_quoting(self):
        def _parse_args(args):
            return iter([f"{arg}\n" for arg in args])

        self.assertEqual(
            swift_compiler_params_processor.process_args(
                [[
                    "swift_worker",
                    "swiftc",
                    "-Xcc",
                    "-I/non/quoted/path",
                    "-Xcc",
                    "-Irelative/path",
                ]],
                parse_args = _parse_args,
            ),
            [
                "-Xcc",
                "-I/non/quoted/path",
                "-Xcc",
                "'-I$(PROJECT_DIR)/relative/path'",
            ],
        )

if __name__ == '__main__':
    unittest.main()
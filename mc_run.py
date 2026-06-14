import subprocess
import os
import json


JAVA_PATH = "javaw"  # or full path to java.exe
MC_DIR = os.path.abspath("./run/")
MC_VERSION = "26.1.2"
ASSET_INDEX = 30

NEO_FORGE_VERSION = "neoforge-26.1.2.64-beta"


def build_classpath(mc_version, neo_forge_version, mc_path=MC_DIR):
    jar_path = os.path.abspath(os.path.join(mc_path, "versions", mc_version, f"{mc_version}.jar"))

    with open(os.path.join(mc_path, "versions", mc_version, f"libraries_{mc_version}.json"), "r") as f:
        mc_libraries = json.load(f)

    with open(os.path.join(mc_path, "versions", neo_forge_version, f"libraries_{neo_forge_version}.json"), "r") as f:
        neo_libraries = json.load(f)

    classpath = ";".join([jar_path] + mc_libraries + neo_libraries)
    return classpath


def run_neo_forge(
        mc_version,
        neo_forge_version,
        asset_index,
        mc_path=MC_DIR,
        instance_path=MC_DIR,
        java_path=JAVA_PATH,
        ram=10
):
    classpath = build_classpath(mc_version, neo_forge_version, mc_path=mc_path)
    username = "Alrza"

    # options = {
    #     "username": username,
    # }

    # command = minecraft_launcher_lib.command.get_minecraft_command(
    #     NEO_FORGE_VERSION,
    #     MC_DIR,
    #     options
    # )

    command = [
        java_path,
        f"-Xmx{ram}G",
        # ATM args
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+UseG1GC",
        "-XX:G1NewSizePercent=20",
        "-XX:G1ReservePercent=20",
        "-XX:MaxGCPauseMillis=50",
        "-XX:G1HeapRegionSize=32M",
        "-XX:+UseStringDeduplication",
        "-XX:+UseCompactObjectHeaders",

        # "-XX:+UseZGC",
        # '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump',
        # '--sun-misc-unsafe-memory-access=allow',
        # '--enable-native-access=ALL-UNNAMED',
        # '-Djava.library.path=E:\\mclaunch\\run\\versions\\neoforge-26.1.2.64-beta\\natives',
        # '-Djna.tmpdir=E:\\mclaunch\\run\\versions\\neoforge-26.1.2.64-beta\\natives',
        # '-Dorg.lwjgl.system.SharedLibraryExtractPath=E:\\mclaunch\\run\\versions\\neoforge-26.1.2.64-beta\\natives',
        # '-Dio.netty.native.workdir=E:\\mclaunch\\run\\versions\\neoforge-26.1.2.64-beta\\natives',
        # '-Dminecraft.launcher.brand=minecraft-launcher-lib',
        # '-Dminecraft.launcher.version=8.0',
        '-cp', # classpath
        classpath,
        # 'E:\\mclaunch\\run\\libraries\\net\\neoforged\\fancymodloader\\earlydisplay\\11.0.13\\earlydisplay-11.0.13.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\fancymodloader\\loader\\11.0.13\\loader-11.0.13.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\accesstransformers\\11.0.2\\accesstransformers-11.0.2.jar;E:\\mclaunch\\run\\libraries\\org\\ow2\\asm\\asm-commons\\9.9.1\\asm-commons-9.9.1.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\mergetool\\2.0.7\\mergetool-2.0.7-api.jar;E:\\mclaunch\\run\\libraries\\org\\ow2\\asm\\asm-util\\9.9.1\\asm-util-9.9.1.jar;E:\\mclaunch\\run\\libraries\\org\\ow2\\asm\\asm-analysis\\9.9.1\\asm-analysis-9.9.1.jar;E:\\mclaunch\\run\\libraries\\org\\ow2\\asm\\asm-tree\\9.9.1\\asm-tree-9.9.1.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\bus\\8.0.5\\bus-8.0.5.jar;E:\\mclaunch\\run\\libraries\\org\\ow2\\asm\\asm\\9.9.1\\asm-9.9.1.jar;E:\\mclaunch\\run\\libraries\\com\\electronwill\\night-config\\toml\\3.8.3\\toml-3.8.3.jar;E:\\mclaunch\\run\\libraries\\com\\electronwill\\night-config\\core\\3.8.3\\core-3.8.3.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\JarJarSelector\\0.5.0\\JarJarSelector-0.5.0.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\JarJarMetadata\\0.5.0\\JarJarMetadata-0.5.0.jar;E:\\mclaunch\\run\\libraries\\org\\apache\\maven\\maven-artifact\\3.9.9\\maven-artifact-3.9.9.jar;E:\\mclaunch\\run\\libraries\\net\\jodah\\typetools\\0.6.3\\typetools-0.6.3.jar;E:\\mclaunch\\run\\libraries\\net\\minecrell\\terminalconsoleappender\\1.3.0\\terminalconsoleappender-1.3.0.jar;E:\\mclaunch\\run\\libraries\\net\\fabricmc\\sponge-mixin\\0.17.3+mixin.0.8.7\\sponge-mixin-0.17.3+mixin.0.8.7.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\accesstransformers\\at-parser\\11.0.2\\at-parser-11.0.2.jar;E:\\mclaunch\\run\\libraries\\org\\jline\\jline-reader\\3.20.0\\jline-reader-3.20.0.jar;E:\\mclaunch\\run\\libraries\\org\\jline\\jline-terminal\\3.20.0\\jline-terminal-3.20.0.jar;E:\\mclaunch\\run\\libraries\\net\\neoforged\\srgutils\\1.0.10\\srgutils-1.0.10.jar;E:\\mclaunch\\run\\libraries\\com\\google\\guava\\listenablefuture\\9999.0-empty-to-avoid-conflict-with-guava\\listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar;E:\\mclaunch\\run\\libraries\\com\\google\\errorprone\\error_prone_annotations\\2.41.0\\error_prone_annotations-2.41.0.jar;E:\\mclaunch\\run\\libraries\\com\\google\\j2objc\\j2objc-annotations\\3.1\\j2objc-annotations-3.1.jar;E:\\mclaunch\\run\\libraries\\org\\codehaus\\plexus\\plexus-utils\\3.5.1\\plexus-utils-3.5.1.jar;E:\\mclaunch\\run\\libraries\\at\\yawk\\lz4\\lz4-java\\1.10.1\\lz4-java-1.10.1.jar;E:\\mclaunch\\run\\libraries\\com\\azure\\azure-json\\1.4.0\\azure-json-1.4.0.jar;E:\\mclaunch\\run\\libraries\\com\\github\\oshi\\oshi-core\\6.9.0\\oshi-core-6.9.0.jar;E:\\mclaunch\\run\\libraries\\com\\google\\code\\gson\\gson\\2.13.2\\gson-2.13.2.jar;E:\\mclaunch\\run\\libraries\\com\\google\\guava\\failureaccess\\1.0.3\\failureaccess-1.0.3.jar;E:\\mclaunch\\run\\libraries\\com\\google\\guava\\guava\\33.5.0-jre\\guava-33.5.0-jre.jar;E:\\mclaunch\\run\\libraries\\com\\ibm\\icu\\icu4j\\77.1\\icu4j-77.1.jar;E:\\mclaunch\\run\\libraries\\com\\microsoft\\azure\\msal4j\\1.23.1\\msal4j-1.23.1.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\authlib\\7.0.63\\authlib-7.0.63.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\blocklist\\1.0.10\\blocklist-1.0.10.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\brigadier\\1.3.10\\brigadier-1.3.10.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\datafixerupper\\9.0.19\\datafixerupper-9.0.19.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\jtracy\\1.0.37\\jtracy-1.0.37.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\jtracy\\1.0.37\\jtracy-1.0.37-natives-windows.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\logging\\1.6.11\\logging-1.6.11.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\patchy\\2.2.10\\patchy-2.2.10.jar;E:\\mclaunch\\run\\libraries\\com\\mojang\\text2speech\\1.18.11\\text2speech-1.18.11.jar;E:\\mclaunch\\run\\libraries\\commons-codec\\commons-codec\\1.19.0\\commons-codec-1.19.0.jar;E:\\mclaunch\\run\\libraries\\commons-io\\commons-io\\2.20.0\\commons-io-2.20.0.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-buffer\\4.2.7.Final\\netty-buffer-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-codec-base\\4.2.7.Final\\netty-codec-base-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-codec-compression\\4.2.7.Final\\netty-codec-compression-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-codec-http\\4.2.7.Final\\netty-codec-http-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-common\\4.2.7.Final\\netty-common-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-handler\\4.2.7.Final\\netty-handler-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-resolver\\4.2.7.Final\\netty-resolver-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-transport-classes-epoll\\4.2.7.Final\\netty-transport-classes-epoll-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-transport-classes-kqueue\\4.2.7.Final\\netty-transport-classes-kqueue-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-transport-native-unix-common\\4.2.7.Final\\netty-transport-native-unix-common-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\io\\netty\\netty-transport\\4.2.7.Final\\netty-transport-4.2.7.Final.jar;E:\\mclaunch\\run\\libraries\\it\\unimi\\dsi\\fastutil\\8.5.18\\fastutil-8.5.18.jar;E:\\mclaunch\\run\\libraries\\net\\java\\dev\\jna\\jna-platform\\5.17.0\\jna-platform-5.17.0.jar;E:\\mclaunch\\run\\libraries\\net\\java\\dev\\jna\\jna\\5.17.0\\jna-5.17.0.jar;E:\\mclaunch\\run\\libraries\\net\\sf\\jopt-simple\\jopt-simple\\5.0.4\\jopt-simple-5.0.4.jar;E:\\mclaunch\\run\\libraries\\org\\apache\\commons\\commons-compress\\1.28.0\\commons-compress-1.28.0.jar;E:\\mclaunch\\run\\libraries\\org\\apache\\commons\\commons-lang3\\3.19.0\\commons-lang3-3.19.0.jar;E:\\mclaunch\\run\\libraries\\org\\apache\\logging\\log4j\\log4j-api\\2.25.2\\log4j-api-2.25.2.jar;E:\\mclaunch\\run\\libraries\\org\\apache\\logging\\log4j\\log4j-core\\2.25.2\\log4j-core-2.25.2.jar;E:\\mclaunch\\run\\libraries\\org\\apache\\logging\\log4j\\log4j-slf4j2-impl\\2.25.2\\log4j-slf4j2-impl-2.25.2.jar;E:\\mclaunch\\run\\libraries\\org\\jcraft\\jorbis\\0.0.17\\jorbis-0.0.17.jar;E:\\mclaunch\\run\\libraries\\org\\joml\\joml\\1.10.8\\joml-1.10.8.jar;E:\\mclaunch\\run\\libraries\\org\\jspecify\\jspecify\\1.0.0\\jspecify-1.0.0.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-freetype\\3.4.1\\lwjgl-freetype-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-freetype\\3.4.1\\lwjgl-freetype-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-freetype\\3.4.1\\lwjgl-freetype-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-freetype\\3.4.1\\lwjgl-freetype-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-glfw\\3.4.1\\lwjgl-glfw-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-glfw\\3.4.1\\lwjgl-glfw-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-glfw\\3.4.1\\lwjgl-glfw-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-glfw\\3.4.1\\lwjgl-glfw-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-jemalloc\\3.4.1\\lwjgl-jemalloc-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-jemalloc\\3.4.1\\lwjgl-jemalloc-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-jemalloc\\3.4.1\\lwjgl-jemalloc-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-jemalloc\\3.4.1\\lwjgl-jemalloc-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-openal\\3.4.1\\lwjgl-openal-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-openal\\3.4.1\\lwjgl-openal-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-openal\\3.4.1\\lwjgl-openal-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-openal\\3.4.1\\lwjgl-openal-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-opengl\\3.4.1\\lwjgl-opengl-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-opengl\\3.4.1\\lwjgl-opengl-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-opengl\\3.4.1\\lwjgl-opengl-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-opengl\\3.4.1\\lwjgl-opengl-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-stb\\3.4.1\\lwjgl-stb-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-stb\\3.4.1\\lwjgl-stb-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-stb\\3.4.1\\lwjgl-stb-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-stb\\3.4.1\\lwjgl-stb-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-tinyfd\\3.4.1\\lwjgl-tinyfd-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-tinyfd\\3.4.1\\lwjgl-tinyfd-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-tinyfd\\3.4.1\\lwjgl-tinyfd-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl-tinyfd\\3.4.1\\lwjgl-tinyfd-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl\\3.4.1\\lwjgl-3.4.1.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl\\3.4.1\\lwjgl-3.4.1-natives-windows.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl\\3.4.1\\lwjgl-3.4.1-natives-windows-arm64.jar;E:\\mclaunch\\run\\libraries\\org\\lwjgl\\lwjgl\\3.4.1\\lwjgl-3.4.1-natives-windows-x86.jar;E:\\mclaunch\\run\\libraries\\org\\slf4j\\slf4j-api\\2.0.17\\slf4j-api-2.0.17.jar;E:\\mclaunch\\run\\versions\\neoforge-26.1.2.64-beta\\neoforge-26.1.2.64-beta.jar',
        # '-Djava.net.preferIPv6Addresses=system',
        f'-DlibraryDirectory={os.path.join(mc_path, 'libraries')}',
        '--add-opens',
        'java.base/java.lang.invoke=ALL-UNNAMED',
        # '--add-exports',
        # 'jdk.naming.dns/com.sun.jndi.dns=java.naming',
        'net.neoforged.fml.startup.Client',
        '--username', username,
        '--version', neo_forge_version,
        '--gameDir', instance_path,
        '--assetsDir', os.path.join(mc_path, 'assets'),
        '--assetIndex', f'{asset_index}',
        '--uuid', '5b7dff45-986f-4804-845f-6da9ab3dedc8',
        '--accessToken', '{token}',
        '--clientId', '${clientid}',
        '--xuid', '${auth_xuid}',
        '--versionType', 'release',
        '--fml.neoForgeVersion', neo_forge_version[9:],
        '--fml.mcVersion', mc_version,
        '--fml.neoFormVersion', '1'
    ]

    env = os.environ.copy()

    # Force NVIDIA GPU
    env["SHIM_MCCOMPAT"] = "0x800000001"
    env["SHIM_RENDERING_MODE"] = "ENABLE"

    subprocess.run(command, cwd=instance_path, env=env)


def main():
    run_neo_forge(MC_VERSION, NEO_FORGE_VERSION, ASSET_INDEX)


if __name__ == "__main__":
    main()

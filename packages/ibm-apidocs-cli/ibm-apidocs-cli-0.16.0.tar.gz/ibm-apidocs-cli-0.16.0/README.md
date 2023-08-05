# ibm-apidocs-cli
![Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Latest Stable Version](https://img.shields.io/pypi/v/ibm-apidocs-cli.svg)](https://pypi.python.org/pypi/ibm-apidocs-cli)

This tool allows users to generate the api documentation.

## Installation

- Install the CLI with `pip` or `easy_install`:

    ```bash
    pip install -U ibm-apidocs-cli
    ```

    or

    ```bash
    easy_install -U ibm-apidocs-cli
    ```

- Clone a [cloud-api-docs](https://github.ibm.com/cloud-api-docs) repo to a local directory. Make sure the repo contains the required `apiref-index.json` file and the front-matter configuration file (typically `<openapi>-config.json`).

- Configure your GitHub Enterprise access token. You can skip this step if you do not want the CLI to automatically download the latest front-matter and SDK generator code.

  Follow these steps:

  1. Get an access token from [GitHub Enterprise](https://github.ibm.com/settings/tokens). For more information, see the [GitHub help](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line).

  1. Set the `GITHUB_TOKEN` environment variable:

    ```
    export GITHUB_TOKEN=<token>
    ```

- **Optional:** Configure a public GitHub access token. The CLI uses the GitHub API to retrieve the latest SDK versions. If you encounter errors caused by exceeding the GitHub API rate limit on anonymous requests, try configuring the public GitHub access token.

  Follow these steps:

  1. Get an access token from [GitHub](https://github.com/settings/tokens). For more information, see the [GitHub help](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line).

  1. Set the `GITHUB_PUBLIC_TOKEN` environment variable:

    ```
    export GITHUB_PUBLIC_TOKEN=<token>
    ```

- **Optional:** Clone the [frontmatter generator](https://github.ibm.com/cloud-doc-build/frontmatter-generator) to a local directory. If you do not have a local clone of the front-matter generator repo, the CLI will automatically clone it to a temporary directory.

- **Optional:** Install the [SDK generator](https://github.ibm.com/CloudEngineering/openapi-sdkgen/releases) to a local directory. If you do not have a local copy of the SDK generator, the CLI will automatically download the latest version to a temporary directory.

  To install the SDK generator, you do not need to clone or download the full repository or build the project. Instead, use the [installer](https://github.ibm.com/CloudEngineering/openapi-sdkgenreleases). For more information, see [the generator README](https://github.ibm.comCloudEngineering/openapi-sdkgen#using-a-pre-built-installer).

  **Note:** The SDK generator .jar file must be named `openapi-sdkgen.jar`. If you have downloaded or built a version of the file with a different name (e.g.`openapi-sdkgen-<version>.jar`), you must rename it.

## Usage

There are two distinct modes of usage:

- **Manual mode** is used to process a single API definition, using a local clone of the `cloud-api-docs` repo for the service. This mode offers fine-grained control, with command-line arguments to specify the front-matter config file and templates, the output location, and other options that are specific to the file being processed. Any required information that is not specified (other than the input API definition) is looked up from the `generate-apidocs.json` map file. Manual mode is the default.

- **Batch mode** is used to process one or more API definitions, specified either individually or using wildcards. With batch mode, processing is largely driven by the map file, which determines the file-specific options for each API definition. You can use optional command-line arguments to specify global options such as the SDK generator to use or the target directory where `cloud-api-docs` repos are located. Batch mode is specified using the `--batch` or `-b` argument.

## Syntax

```text
usage: ibm-apidocs-cli [-h | --help]
                       [--batch | -b]
                       -i <input_openapi> | --openapi <input_openapi>
                       [--config <config_file>]
                       [--mapfile <map_file>]
                       [--apidocs <apidocs_path>]
                       [--templates <templates_path>]
                       [--examples <examples_path>]
                       [--output_folder <output_path>]
                       [--target <target>]
                       [--frontmatter <frontmatter_path>]
                       [--sdk_generator <sdk_generator_path>]
                       [--sdkgen_release <sdkgen_release>]
                       [--commit_msg <commit_message>]
                       [--push] [--keep_sdk] [--keep_temp]
                       [--no_update] [--verbose] [--version]
```

Required arguments:

- `-i, --openapi <openapi_file>`: The path to the input OpenAPI definition file(s) to process:

  - In manual mode, this must be exactly one file (for example, `assistant-v1.json`).

  - In batch mode, this can be one or more file names or patterns, separated by spaces. Any pattern containing wildcards will be expanded. For example, `./apis-public/*.json ./apis-private/*data*.json` would process all files in the `apis-public` subdirectory and all files matching the pattern `*data*.json` in the `apis-private` subdirectory.

    **Note:** If you specify a path that contains wildcards, do not surround it with quotation marks. Use a backslash (`\`) to escape spaces in the path.

  Only files that are defined in the mapping file are processed. Any file not in the mapping file is skipped, and processing continues.

Optional arguments:

- `-h, --help`: Display usage information.

- `-b, --batch`: Batch mode switch. Use batch mode to process multiple files at once, using the map file to automatically look up required values on a per-file basis. The default is manual mode, which offers more fine-grained control over options but can process only one file at a time.

  **Note:** The handling of some command-line arguments, as well as which arguments are valid, differ between batch mode and manual mode, as described in this document.

- `--config <config_file>` _(Manual mode only)_: The front-matter config file (e.g. `assistant-v1-config.json`). You can optionally specify the full path to the config file; if you do not include the path, the file is assumed to be in the `apidocs` directory. If you do not specify the config file, the file name is looked up from the map file, and the file is assumed to be in the `apidocs` directory.

  In batch mode, the config file name is always looked up from the map file and retrieved from the downloaded `cloud-api-docs` repo for the service.

- `--apidocs <apidocs_path>` _(Manual mode only)_: The path to the `cloud-api-docs` repository or other directory containing `apiref-index.json` and front matter config file. If you do not specify this argument, the current directory is used. In batch mode, you can use the `--target` argument to use local `cloud-api-docs` repos.

- `--templates <templates_path>` _(Manual mode only)_: Path to the directory containing the front-matter templates to use. You can specify either an absolute path or just the directory name (for example, `templates-data`); if you specify just the directory name, it is assumed to be a subdirectory of the front-matter generator location. If you do not specify a templates directory, the CLI will use the templates directory specified in the map file.

  In batch mode, the templates directory for each API definition is looked up from the map file.

- `--examples <examples_path>` Path to the directory containing the example files associated with the input OpenAPI definition(s). This is typically the `examples` directory of a local clone of the `developer-cloud--api-definitions` repo). If you do not specify an examples directory, the CLI will download the example files from the `developer-cloud--api-definitions` GHE repo. In batch mode, the same examples directory is used for all API definitions.

  The specific example files to be copied to the output directory for a given OpenAPI file are listed in the map file. If the `examples` array is empty or absent for the input API definition, no example files are copied.

- `--output_folder <output_folder>` _(Manual mode only)_: The output directory for generated files. If you do not specify this argument, output files are written to the current directory. In batch mode, you can use the `--target` argument to control the location for generated files.

- `--target <target>` _(Batch mode only)_: The parent directory of the local `cloud-api-docs` repos you want to use for config files and output. The CLI will look for subdirectories of this directory named according to the service names listed in the map file, which correspond to the `cloud-api-docs` repo names (for example, `watson-assistant` or `discovery`). If the expected subdirectory is not present, the CLI will clone it from GHE.

  **Important:** If the `cloud-api-docs` directory for an affected service already exists as a subdirectory of the `target` location, the CLI uses it as-is. The config file might be modified, and the generated files will overwrite previous versions that are already present. Keep in mind that if this directory is not current, you might not be able to push the changes to GHE without conflicts. It is your responsibility to make sure any existing `cloud-api-docs` directories are current, or that they contain only changes you want. (You can also delete any existing `cloud-api-docs` directory and allow the CLI to clone the current version from GHE.)

  If you omit the `--target` argument in batch mode, the `cloud-api-docs` directories for the affected services are cloned to a temporary location. This means that the output is discarded after processing completes (unless you specify the `--keep_temp` argument). This can still be useful if you want to run a test build to check for build errors, but do not need to see the generated output.

- `--mapfile <map_file>`: The path to a local map file, including file name (for example, `generate-apidocs.json`). If you do not specify a local map file, the current map file is downloaded from the `developer-cloud--api-definitions` repo as needed.

- `--frontmatter <frontmatter_path>`: Path to the directory containing the front-matter generator `app.js` file. Use this option if you need to use a specific version or branch of the front-matter generator code, or if you do not have a GitHub access token configured. If you do not specify a location, the CLI will automatically clone the latest version of the front-matter generator repo to a temporary directory and use that clone.

- `--sdk_generator <sdk_generator_path>`: Path to the directory containing the SDK generator JAR file, optionally including the file name. If you specify a directory but not a file name, the JAR file is assumed to be `openapi-sdkgen.jar`. Use this option if you need to use local copy of the SDK generator. If you do not specify this parameter, the CLI will automatically download the the `openapi-sdkgen.jar` file to a temporary directory and use that copy.

- `--sdkgen_release <sdkgen_release>`: Release of the SDK generator to download, if you are allowing the CLI to download the generator automatically. Specify the GitHub release tag (for example, `1.0.0.1`). If you do not specify a release, the CLI uses the most recent maintenance release for the major release specified in the map file. This argument is ignored if `--sdk_generator` is specified.

- `--commit_msg <commit_message>`: _(Batch mode only)_ Custom commit message to use when pushing generated files to the `cloud-api-docs` repo for the service. (Ignored if `--push` is not also specified.) If you do not specify a custom commit message, the default commit message is `Commit by ibm-apidocs-cli: build <oas3_file>`.

- `--push`: _(Batch mode only)_ Commit and push generated files to the `master` branch of the remote GitHub `cloud-api-docs` repo for the service.

  **Important:** This feature uses the `git add`, `git commit`, and `git push` commands to push the local target directory (where files are generated) to GitHub. If you are using the `--target` argument to generate files in an existing local directory, that directory _must_
  be an up-to-date valid local clone of a remote api-docs repo, with the `master` branch
  checked out.

  The safest way to use the `--push` option is to omit the `--target` argument. This ensures that the generated files are written to a freshly cloned local repo, which is guaranteed to be even with the remote.

- `--keep_sdk`: Preserve the `_sdktemp` directory containing generated SDK artifacts. Useful for debugging purposes.

- `--keep_temp`: Preserve the temporary directory containing the downloaded front-matter and SDK generators, as well as any `cloud-api-docs` repos downloaded during batch processing. Useful for debugging purposes.

- `--no_update`: Use front-matter config file as-is without updating SDK versions. If you do not specify this argument, the config file is updated with the latest GitHub release for each supported SDK language.

- `-h`, `--help`: Show usage information and exit.

- `--verbose`: Verbose flag.

- `--version`: Show program's version number and exit.

### Example commands: manual mode

This example assumes that the command is being run from the `apidocs` repo directory containing the API Reference files, and that the CLI is automatically downloading and using the latest code for the front-matter and SDK generators. All output files are written to the current directory:

```bash
ibm-apidocs-cli -i assistant-v1.json
```

This example uses different locations for the input and output files, and also specifies local copies of the SDK generator and front-matter generator code:

```
ibm-apidocs-cli -i '/Users/my_user/Documents/GitHub/api-apidocs-cli/test/resources/config/assistant-openapi3-v1.json' \
                -c '/Users/my_user/Documents/GitHub/api-apidocs-cli/test/resources/config/test-input-config.yaml' \
                --output_folder '/Users/my_user/Documents/GitHub/api-apidocs-cli/test/target' \
                --frontmatter '/Users/my_user/Documents/GitHub/frontmatter-generator' \
                --sdk_generator '/Users/my_user/Documents/Release/openapi-sdkgen/lib'
```

### Example commands: batch mode

This example builds two API definitions from the current directory. All other required files, including the map file, the `cloud-api-docs` repo, the front-matter generator, and the SDK generator, are downloaded automatically. Output is written to the temporary `cloud-api-docs` directory and is not kept.

```
ibm-apidocs-cli -b -i assistant-v1.json assistant-v2.json
```

This example builds all API definitions from the `public` and `private` subdirectories, using local copies of the `cloud-api-docs` subdirectories for the affected services. Generated files will be written to these same subdirectories.

```
ibm-apidocs-cli -b ./apis-public/*.json ./apis-private/*.json --target ~/github/cloud-api-docs
```

## Mapping file

The `generate-apidocs.json` mapping file is a configuration file that is used by `ibm-apidocs-cli` to determine various default values for each API definition.

The canonical version of this file is located in the root of the [developer-cloud--api-definitions](https://github.ibm.com/Watson/developer-cloud--api-definitions/blob/master/generate-apidocs.json) repo. By default, the CLI downloads and uses the current mapping file from GitHub, but you can use the `--mapfile` argument to specify a local mapping file.

The format of the mapping file is as follows:

```
{
  "name": "api-mapping",
  "version": "0.1.0",
  "sdkgen_major_release": "2",
  "description": "api document mapping used by ibm-apidocs-cli tool",
  "public": [
    {
      "service": "watson-assistant",
      "openapi": "assistant-v1.json",
      "config": "assistant-v1-config.json",
      "frontmatter": "templates",
      "examples": [
        "assistant-v1-curl-examples.json",
        "assistant-v1-dotnet-standard-examples.json",
        "assistant-v1-go-examples.json",
        "assistant-v1-java-examples.json",
        "assistant-v1-node-examples.json",
        "assistant-v1-python-examples.json",
        "assistant-v1-ruby-examples.json",
        "assistant-v1-swift-examples.json",
        "assistant-v1-unity-examples.json"
      ]
    },
    ...
  ],
  "private": [
    {
      "service": "watson-assistant",
      "openapi": "assistant-data-v1.json",
      "config": "assistant-v1-config.json",
      "frontmatter": "templates-data",
      "examples": [
        "assistant-v1-curl-examples.json",
        "assistant-v1-dotnet-standard-examples.json",
        "assistant-v1-go-examples.json",
        "assistant-v1-java-examples.json",
        "assistant-v1-node-examples.json",
        "assistant-v1-python-examples.json",
        "assistant-v1-ruby-examples.json",
        "assistant-v1-swift-examples.json",
        "assistant-v1-unity-examples.json"
      ]
    },
    ...
  ]
}
```

where:

- `name`: An identifier for the mapping file. This value is not used by the CLI.

- `version`: The mapping file version. This value is not used by the CLI.

- `sdkgen_major_release`: A global configuration value identifying the major version of the [SDK generator](https://github.ibm.com/CloudEngineering/openapi-sdkgen/releases) that was used to generate the currently available SDKs. The `ibm-apidocs-cli` script uses this value to determine which `sdkgen` version to use for generating language-specific files. (By default, the most recent maintenance release for the configured major release is used.)

- `description`: Description of the mapping file. This value is not used by the CLI.

- `public`: An array of JSON objects describing OAS3 API definitions for public Watson services. These are the OAS3 files in the `apis-public` directory of the [developer-cloud--api-definitions](https://github.ibm.com/Watson/developer-cloud--api-definitions) repo.

- `private`: An array of JSON objects describing OAS3 API definitions for private (ICP and ICP4D) Watson services. These are the OAS3 files in the `apis-private` directory of the [developer-cloud--api-definitions](https://github.ibm.com/Watson/developer-cloud--api-definitions) repo.

Within the `public` and `private` arrays, each object maps an API definition to the default values used by `ibm-apidocs-cli`:

- `service`: An identifier for the Watson service described by the OAS3 file. This identifier is the same as the name of the [`cloud-api-docs`](https://github.ibm.com/cloud-api-docs) repo for the service, and is used to clone repos and push generated files to GHE.

- `openapi`: The name of the OAS3 file in the `apis-public` or `apis-private` directory.

- `config`: The name of the front-matter configuration file to use when building the API Reference for the OAS3 file. The specified configuration file is assumed to exist in the `cloud-api-docs` repo for the service.

- `frontmatter`: The name of the directory containing the front-matter templates to use when building the API Reference for the OAS3 files. The specified directory must exist in the [frontmatter-generator](https://github.ibm.com/cloud-doc-build/frontmatter-generator) repo.

- `examples`: An array listing the names of the JSON files containing request examples to be merged with the OpenAPI definition at build time. The listed example files will be copied to the output directory along with the input OpenAPI file.

## Python version

✅ Tested on Python 3.5, 3.6, and 3.7.

## Contributing

See [CONTRIBUTING.md][CONTRIBUTING].

## License

MIT

[ibm_cloud]: https://cloud.ibm.com
[responses]: https://github.com/getsentry/responses
[requests]: http://docs.python-requests.org/en/latest/
[CONTRIBUTING]: ./CONTRIBUTING.md

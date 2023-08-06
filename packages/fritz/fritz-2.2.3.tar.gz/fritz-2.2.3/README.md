# Fritz CLI

Mobile machine learning projects can be messy. By the time an app is ready to ship, it’s not uncommon to have trained hundreds of models experimenting with different architectures, hyperparameters, and formats. Keeping all of these assets organized for rapid prototyping and evaluation is the key to delivering better mobile apps in less time. The Fritz CLI lets you manage all of your mobile machine learning models and and easily evaluate their in-app performance right from your terminal.

### Create a Fritz Account

[Sign up for an account](https://app.fritz.ai/register) and [follow these directions](https://docs.fritz.ai/cli/index.html#install) in order to use the CLI.

### Setup

You can install the CLI tool with

```
$ pip install fritz
$ fritz config update \
    --api-key <Your API Key will be here> \
    --project-id <Your Project ID will be here>
```

### Usage

With the Fritz CLI, you can:

- See all of the models you have trained and uploaded to Fritz.
- View model configurations and metadata for any specific version of a model.
- Upload and download model checkpoints to and from Fritz.
- Deploy new model versions to a mobile app without releasing a new build.
- Automatically set up a new Xcode or Android Studio project for mobile machine learning with Fritz.

We’ve made all of these capabilities available directly from the command line to streamline your workflow and reduce the need to switch between tools.

For more examples, visit [our docs site](https://docs.fritz.ai/cli/index.html).

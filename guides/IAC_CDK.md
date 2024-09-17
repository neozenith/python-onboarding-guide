# AWS CDK

This micro blog will cover all the fun little pieces I collate along the way about AWS CDK for Infrstructure as Code.

<!--TOC-->

- [AWS CDK](#aws-cdk)
  - [Quickstart](#quickstart)
  - [Automating Diagrams](#automating-diagrams)
    - [`Makefile` snippet:](#makefile-snippet)
    - [Markdown Snippet](#markdown-snippet)

<!--TOC-->


## Quickstart

```sh
npm install -g aws-cdk
```

## Automating Diagrams

This makes use of [`cdk-dia`](https://github.com/pistazie/cdk-dia) as well as `npx` to make a one off install of the tooling outside of project dependencies.

### `Makefile` snippet:

```Makefile
docs: .make/dev-deps-installed cdk-synth
	npx cdk-dia --rendering "graphviz-png" --target docs/diagrams/diagram-simple.png --collapse true --collapse-double-clusters true
	npx cdk-dia --rendering "graphviz-png" --target docs/diagrams/diagram-detailed.png --collapse false --collapse-double-clusters false

	npx cdk-dia --rendering "cytoscape-html" --target docs/diagrams/ --collapse false --collapse-double-clusters false 
```

### Markdown Snippet

```md
<details>
    <summary><i>Click this arrow for detailed diagram</i>
        <h4>Architecture Diagram: Simple</h4>
        <img src="docs/diagrams/diagram-simple.png" alt="Architecture Diagram: Simple" width="100%" />
    </summary>
    <h4>Architecture Diagram: Detailed</h4>
    <img src="docs/diagrams/diagram-detailed.png" alt="Architecture Diagram: Detailed" width="100%" />
</details>
```

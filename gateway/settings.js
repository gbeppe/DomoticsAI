module.exports = {
    flowFile: 'flows.json',
    flowFilePretty: true,
    credentialSecret: false,
    adminAuth: undefined,
    uiPort: process.env.PORT || 1881,
    functionGlobalContext: {},
    contextStorage: {
        default: {
            module: "localfilesystem"
        }
    },
    exportGlobalContextKeys: false,
    logging: {
        console: {
            level: "info",
            metrics: false,
            audit: false
        }
    },
    editorTheme: {
        projects: {
            enabled: true,
            workflow: {
                mode: "manual"
            }
        }
    }
};

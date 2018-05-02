let fs = require('fs')
let rimraf = require('rimraf')
let theia_path = __dirname +  "\\node_modules\\@theia"


if (fs.existsSync(__dirname + "\\symlinks.json")) {
    let content = fs.readFileSync(__dirname + "\\symlinks.json")
    var symlinks = JSON.parse(content);

    for (let symlink in symlinks) {
        filepath = theia_path + "\\" + symlink
        
        if (fs.existsSync(filepath)) {
            stats = fs.lstatSync(filepath)
            if (stats.isSymbolicLink()) {
                fs.unlinkSync(filepath)
            }else {
                rimraf.sync(filepath)
            }
        }
        fs.symlinkSync(symlinks[symlink], filepath,"junction")
    }
    process.exit()
}
symlinks = {}

files = fs.readdirSync(theia_path);
files.push("..\\@deepcognition\\auth")
files.forEach(element => {
    let filepath = theia_path + "\\" + element
    let stats = fs.lstatSync (filepath)
    if (stats.isSymbolicLink()) {
        let target = fs.readlinkSync (filepath)

        new_target = target.replace(__dirname,"..\\..")
        fs.unlinkSync(filepath)
        symlinks[element] = new_target
    }
});

fs.writeFileSync(__dirname + "\\symlinks.json", JSON.stringify(symlinks))


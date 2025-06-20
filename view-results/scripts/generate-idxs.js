const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '../../results/yolo_results/');
const files = fs.readdirSync(dir);

const baseNames = files
  .filter(file => file.endsWith('.jpg'))
  .map(file => path.basename(file, '.jpg'))
  .filter(name => fs.existsSync(path.join(dir, name + '.txt')));

fs.writeFileSync(
  path.join(__dirname, '../public/yolo_data_index.json'),
  JSON.stringify(baseNames, null, 2)
);

console.log("Index generated.");


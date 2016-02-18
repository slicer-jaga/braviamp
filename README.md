# braviamp
Scripts for remote control *Sony Bravia Television* and running media portal application on TV.

* `tv.py` - TV remote control. 
* `toTV.cmd` - run mediaportal application ([KODI](http://kodi.tv/) as default) on TV.
* `tvServ.py` - debug server.

## Setup TV remote control
* `tv.py`: Replace `TVIP`, `TVMAC` variables by your own values.
* Enable Simple IP Control on your TV options: `Network > Home Network Setup > IP Control > Simple IP Control`
## Setup mediaportal
* `toTV.cmd`: Replace `MEDIAPORTALINPUT` no your TV-to-PC connection. See `setInput` function in [spec](http://shop.kindermann.com/erp/KCO/avs/3/3005/3005000168/01_Anleitungen+Doku/Steuerungsprotokoll_1.pdf) for details. Sample: `100000001` - is HDMI1, `100000002` - HDMI2, etc.
* `toTV.cmd`: As require, you may replace `MEDIAPORTALPATH`, `MMEDIAPORTALEXE`, `MEDIAPORTALVOLUME` by your values.

## Usage
* Show help
```
$ ./tv.py -?
```
* [Simple IP Specification](http://shop.kindermann.com/erp/KCO/avs/3/3005/3005000168/01_Anleitungen+Doku/Steuerungsprotokoll_1.pdf).

## License
Licensed by [GNU General Public License](http://www.gnu.org/licenses/gpl.html).
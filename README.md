
# Bing Daily Wallpaper Updator Ubuntu

Bing Daily Wallpaper Updator is a software that update wallpaper daily. You can use by both ways through command line or through GUI.




## Screenshots

![Screenshot 1](https://user-images.githubusercontent.com/51308210/185895834-c832da30-040b-47c9-b2e6-e375ca5352f1.png)

![Screenshot 2](https://user-images.githubusercontent.com/51308210/185912988-8853a426-42a0-4433-98b0-9b7093c7ec0f.png)
## API
Api address : [https://bing.biturl.top](https://bing.biturl.top/)

## Parameters
`resoultion` The default resolution of the image is `1920`. You can use `1366` (720p Resolution) or `3840` (4k Resolution).

`format` It return json file. Which constains `start_date`, `end_date`, `url`(image url), `copyright` and `copyright_link`.

### Example

* Request

```text
https://bing.biturl.top/?resolution=1920&format=json&index=0&mkt=en-US
```

* Response

```json
{   
    "start_date":"20220822",
    "end_date":"20220823",
    "url":"https://www.bing.com/th?id=OHR.TenderMoment_EN-US3269942524_1920x1080.jpg",
    "copyright":"A burrowing owl chick and adult in South Florida (© Carlos Carreno/Getty Images)",
    "copyright_link":"https://www.bing.com/search?q=burrowing+owl\u0026form=hpcapt\u0026filters=HpDate%3a%2220220822_0700%22"
}
```
## Installation

There is no need to install this program. You can simply download and use.
    
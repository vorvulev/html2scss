# html2scss

This plugin parse your html and puts its scss rules(grouped by classes) into clipboard.

## Usage

The package provide 1 command - `html2scss` with 1 optional argument - `all_attrs = False`. You can use it with shortcut or run from command palette(`html2scss`)

After you run the command in your html file, you'll see message in status bar: `scss rules copied!`. By default all file will be parsed, but you can select any region you need.

Now you can paste the rules in your scss file with `Ctrl+v`

## Example

Input html:
```html
<div class="class1">
	<div class="class2" id="id2" >
		<div>
			<div class="class5"></div>
			<div class="class3 cls3 cls3--mod" test></div>
			<div class="class3 otherClass"></div>
			<div class="class3 cls3" data-attribute attr="simple" test></div>
			<div class="class4"></div>
			<div class="class4"></div>
			<a href="#"></a>
		</div>
	</div>
</div>
```
Result rules:
```scss
.class1 {

	#id2.class2 {

		.class5 {
		}

		.class3 {

			&.cls3 {

				&.cls3--mod {
				}
			}

			&.otherClass {
			}
		}

		.class4 {
		}
	}
}
```
Result rules with `all_attrs`:
```scss
.class1 {

	#id2.class2 {

		.class5 {
		}

		.class3 {

			&.cls3 {

				&.cls3--mod[test] {
				}

				&[data-attribute][attr="simple"][test] {
				}
			}

			&.otherClass {
			}
		}

		.class4 {
		}
	}
}
```

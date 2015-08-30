

function reveal() {
  newfield = '<label for="category">category</label><input class="form-control" id="category" name="category" size="20" type="text" value="" placeholder="new category name">'
  $('.hide-it').html(newfield)
  console.log('asdf')
}
$( "#newCategory" ).on( "click", reveal );
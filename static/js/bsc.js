

class window.LoadingSpinner
  
  constructor: ($container, options) ->
    
    # set default options
    defaults = {
      fadeDuration: 300
    }
    
    # override the defaults with the passed in options
    @options = $.extend(defaults, options)
    
    # create the spinner and add it to the container
    @$spinner = $("<div>").addClass("loadingSpinner")
    $container.append(@$spinner)
    @$spinner.hide().fadeIn(@options.fadeDuration)
  
  
  destroy: ->
    
    @$spinner.fadeOut(@options.fadeDuration, =>
      @$spinner.remove()
      @$spinner = null
    )






class window.SpinnerButton
  
  constructor: (@$button, @clickCallback, options) ->
    
   
    defaults = {
      buttonContentTag: "span",
      fadeDuration: 300,
      classDuringLoading: "spinning"
    }
    
    
    @options = $.extend(defaults, options)
    
    
    if @$button.children().length == 1
      @$childContent = $(@$button.children()[0])
    else
      
      @$childContent = $("<#{@options.buttonContentTag}>")
      
      if @$button.children().length > 1
        @$childContent.append(@$button.children())
      else
        @$childContent.text(@$button.text())
        @$button.text("")
      
      @$button.append(@$childContent)
    
    if @clickCallback? then @$button.click(( => @handleClick() ))
  
  
  handleClick: ->
    
    @start()
    
    if @clickCallback? then @clickCallback() else return true
  
  
  start: ->
    
    
    @$button.addClass(@options.classDuringLoading)
    @$childContent.animate({opacity: 0}, @options.fadeDuration)
    @spinner = new LoadingSpinner(@$button, { fadeDuration: @options.fadeDuration })
    

    @$button.prop("disabled", "true")
  
  
  stop: ->
    
    # fade back in the existing button content and destroy the loading spinner
    @$childContent.animate({opacity: 1}, @options.fadeDuration)
    @spinner.destroy()
    @spinner = null
    
    # re-enable the button and remove its class
    @$button.prop("disabled", "")
    @$button.removeClass(@options.classDuringLoading)




# ---------------------- usage -----------------------

$(document).ready( ->
  
  # create a spinnerButton
  spinnerButton = new SpinnerButton($("button"), ->
    
    # run code on click
    
    # you can stop the button by calling .stop()
    setTimeout( ->
      spinnerButton.stop()
    , 1000)
  )
)
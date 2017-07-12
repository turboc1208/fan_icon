#####################################################
#        
#  fan_icon.py
#
#  Set image on fan sensors to show state.
#
#  Appdaemon.yaml file
#  fan_icon:
#    class: fan_icon
#    module: fan_icon
#    img_low: "/local/fan_green.jpg"
#    img_medium: "/local/fan_green.jpg"
#    img_high: "/local/fan_green.jpg"
#######################################################
import appdaemon.appapi as appapi
               
class fan_icon(appapi.AppDaemon):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("fan_icon App")
    self.listen_state(self.state_handler,"fan")
    if "img_low" in self.args:
      self.img_low=self.args["img_low"]
    else:
      self.log("img_low must be defined in appdaemon configuration files")
    if "img_medium" in self.args:
      self.img_medium=self.args["img_medium"]
    else:
      self.log("img_medium must be defined in appdaemon configuration files")
    if "img_high" in self.args:
      self.img_high=self.args["img_high"]
    else:
      self.log("img_high must be defined in appdaemon configuration files")



  def state_handler(self,entity,attribute,old,new,kwargs):
    self.log("{} changed".format(entity))
    etyp,ename=self.split_entity(entity)
    current_state=self.get_state(entity,"all")
    self.log("etyp={}, state={}".format(etyp,current_state))
    if etyp=="fan":
      if current_state["state"] in ["on","high","low","medium"]:
        current_speed=current_state["attributes"]["speed"]
        if current_speed=="low":
          img=self.img_low
        elif current_speed=="medium":
          img=self.img_medium
        elif current_speed=="high":
          img=self.img_high
        else:
          self.log("Unknown speed {}".format(current_speed))
        self.log("Setting state to on for {}-{}".format(entity,img))
        self.set_state(entity,attributes={"entity_picture":img})

//
//  ViewController.h
//  moes
//
//  Created by Mobile Action Lab on 12/4/12.
//  Copyright (c) 2012 Youth Radio. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController {
    UIButton *kurt;
}

@property (nonatomic, strong) IBOutlet UIButton *kurt;

-(IBAction)doSomething:(id)sender;

@end
